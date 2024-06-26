from django.shortcuts import render
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse,HttpResponseRedirect,HttpResponseNotFound
from math import ceil
import logging
from django.urls import reverse
logger = logging.getLogger('course')

from .models import *


def get_lesson(request, slug):
    lesson = Lesson.objects.get(slug=slug)
    if request.method == 'POST':
        name = (request.POST.get('name')).strip()
        if name :
            email = (request.POST.get('email')).strip()
            comment = (request.POST.get('comment')).strip()
            LessonComment.objects.create(name=name,email=email,content=comment,lesson=lesson)
    context = {
       'lesson' : lesson
    }
    context["user"] = request.user.id
    context['comments'] = LessonComment.objects.filter(lesson=lesson,checked=True).order_by('-id')
    context["rate"] = LessonRates.objects.filter(user=request.user.id,lesson=lesson)
    if request.user.id :
        temp = lesson 
        attend = Attend.objects.get(user=request.user,course=lesson.course)
        lessons = Lesson.objects.filter(course=lesson.course).count()
        lesson = Lesson.objects.filter(course=lesson.course)
        i = ceil(attend.progress * lessons / 100)
        if i != lessons:
            if lesson[i] == temp:
                i += 1
                attend.progress = i/lessons * 100
                attend.save()
    return render(request,'course/lesson.html',context)
 


class CourseListView(ListView):
    # paginate_by = 5

    def get(self, request):
        context = {}
        context['user'] = request.user.id
        context ['new_courses'] = Course.objects.order_by('-date')[:5]
        context ['popular_courses'] = Course.objects.order_by('-score')[:5]
        context ['best_courses'] = Course.objects.order_by('-attends')[:5]
        context ['course_list'] = Course.objects.order_by('date')
        return render(request,'course/course_list.html',context)



def CourseDetailView(request, slug):
    course = Course.objects.get(slug=slug)
    if request.method == 'POST':
        name = (request.POST.get('name')).strip()
        email = (request.POST.get('email')).strip()
        comment = (request.POST.get('comment')).strip()
        CourseComment.objects.create(name=name,email=email,content=comment,course=course)
    prof = course.professor.all()
    lessons = Lesson.objects.filter(course=course.id)
    comments = CourseComment.objects.filter(course=course,checked=True).order_by('-id')
    # commentanswer = CourseCommentAnswer.objects.filter(comment=comment)
    context={
        'course': course, 'prof': prof, 'lessons': lessons, 'comments': comments,
        # 'commentanswer':commentanswer,
    }
    context["user"] = request.user.id
    context["rate"] = CourseRates.objects.filter(user=request.user.id,course=course)
    attend = Attend.objects.filter(user=request.user.id,course=course)[:1]
    if attend:
        context["attend"] = list(Attend.objects.filter(user=request.user.id,course=course)[:1])[0]
    return render(request,'course/course_detail.html',context)



@login_required(login_url='/user/login/')
def continue_course(request, **kwargs):
    try:
        course = request.POST.get('course_id')
        pk = request.POST.get('attend_id')
        attend = Attend.objects.get(id=pk)
        lessons = Lesson.objects.filter(course=course).count()
        i = ceil((int(attend.progress) * lessons) / 100)
        if i == lessons:
            return HttpResponse('you complete the course')
        lesson = Lesson.objects.filter(course=course)
        if lesson[i]:
            return get_lesson(request, lesson[i].slug)
        else:
            return HttpResponse('you complete the course')
    except Exception as e:
        logger.warning(f'continue_course view: {str(e)}')
        return HttpResponseNotFound("A problem occurred. please try again later")         


@login_required(login_url='/user/login/')
def add_course(request, **kwargs):
    user = request.user
    course_id = request.POST.get('course_id')
    course = Course.objects.get(id=course_id)
    user_objects = Attend.objects.filter(user=user)
    for c in user_objects:
        if c.course == course:
            return HttpResponse('you attended in this course')
    Attend.objects.create(user=user,course=course)
    if course.add_attend():
        return HttpResponseRedirect(reverse('course_details', args=[course.slug]))



class CategoryListView(ListView):
    model = Category
    context_object_name = 'category_list'
    template_name = 'course/category_list.html'


    def get(self, request):
        context = {}
        attend = []
        context['user'] = request.user.id
        context ['category_list'] = Category.objects.all()
        for c in context ['category_list']:
            course = Course.objects.filter(category=c)
            a = 0
            for i in course:
                a += i.attends
            attend.append(a)
        zipped_catlist = zip(attend,context['category_list'])
        context ['attend'] = attend
        context ['zipped_catlist'] = zipped_catlist
        context ['popular'] = Category.objects.order_by('-score')[:5]
        attend = []
        for c in context ['popular']:
            course = Course.objects.filter(category=c)
            a = 0
            for i in course:
                a += i.attends
            attend.append(a)
        zipped_poplist = zip(attend,context['popular'])
        context ['zipped_poplist'] = zipped_poplist

        return render(request, 'course/category_list.html',context)


def category_courses(request, slug):
    cat = Category.objects.get(slug=slug)
    context={
        'title':slug,
    }
    context["user"] = request.user.id
    context ['new_courses'] = Course.objects.filter(category=cat).order_by('-date')
    context ['popular_courses'] = Course.objects.filter(category=cat).order_by('-score')[:5]
    context ['best_courses'] = Course.objects.filter(category=cat).order_by('-attends')[:5]
    context ['course_list'] = Course.objects.filter(category=cat).order_by('date')
    return render(request,'course/category_courses.html',context)



@login_required(login_url='/user/login/')
def like_coursecomment(request,id):
    comment = CourseComment.objects.get(id=id)
    if not comment.likes.filter(id=request.user.id).exists():
        comment.likes.add(request.user)
        if comment.dislikes.filter(id=request.user.id).exists():
            comment.dislikes.remove(request.user)
    else:
        comment.likes.remove(request.user)
    slug = comment.course.slug
    return HttpResponseRedirect(reverse('course_details', args=[slug]))


@login_required(login_url='/user/login/')
def dislike_coursecomment(request, id):
    comment = CourseComment.objects.get(id=id)
    if not comment.dislikes.filter(id=request.user.id).exists():
        comment.dislikes.add(request.user)
        if comment.likes.filter(id=request.user.id).exists():
            comment.likes.remove(request.user)
    else:
        comment.dislikes.remove(request.user)
    slug = comment.course.slug
    return HttpResponseRedirect(reverse('course_details', args=[slug]))


@login_required(login_url='/user/login/')
def like_lessoncomment(request,id):
    comment = LessonComment.objects.get(id=id)
    if not comment.likes.filter(id=request.user.id).exists():
        comment.likes.add(request.user)
        if comment.dislikes.filter(id=request.user.id).exists():
            comment.dislikes.remove(request.user)
    else : 
        comment.likes.remove(request.user)
    slug = comment.lesson.slug
    return HttpResponseRedirect(reverse('get_lesson', args=[slug]))


@login_required(login_url='/user/login/')
def dislike_lessoncomment(request, id):
    comment = LessonComment.objects.get(id=id)
    if not comment.dislikes.filter(id=request.user.id).exists():
        comment.dislikes.add(request.user)
        if comment.likes.filter(id=request.user.id).exists():
            comment.likes.remove(request.user)
    else:
        comment.dislikes.remove(request.user)
    slug = comment.lesson.slug
    return HttpResponseRedirect(reverse('get_lesson', args=[slug]))
