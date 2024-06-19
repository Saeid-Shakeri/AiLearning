from django.shortcuts import render
from django.views.generic import ListView, View
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from math import ceil
from .models import *



def get_lesson(request, slug):
    lesson = Lesson.objects.get(slug=slug)
    context = {
        'lesson' : lesson
    }
    context["user"] = request.user.id
    return render(request,'course/lesson.html',context)


class CourseListView(ListView):
    # paginate_by = 5

    def get(self, request):
        context = {}
        context['user'] = request.user.id
        context ['new_courses'] = Course.objects.order_by('-date')
        context ['popular_courses'] = Course.objects.order_by('-score')[:5]
        context ['best_courses'] = Course.objects.order_by('-attends')[:5]
        context ['course_list'] = Course.objects.order_by('date')
        return render(request,'course/course_list.html',context)




def CourseDetailView(request, slug):
    course = Course.objects.get(slug=slug)
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        comment = request.POST.get('comment')
        CourseComment.objects.create(name=name,email=email,content=comment,course=course)
    prof = course.professor.all()
    lessons = Lesson.objects.filter(course=course.id)
    comments = CourseComment.objects.filter(course=course).order_by('-id')
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
    course = request.POST.get('course_id')
    user = request.user.id
    pk = request.POST.get('attend_id')
    attend = Attend.objects.get(id=pk)
    lessons = Lesson.objects.filter(course=course).count()
    i = ceil(attend.progress * lessons / 100)
    i -= 1
    lesson = Lesson.objects.filter(course=course)
    lesson[i].slug
    return get_lesson(request, lesson[i].slug)



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
        return HttpResponse('the course added to your profile')


class CategoryListView(ListView):
    model = Category
    context_object_name = 'category_list'
    template_name = 'course/category_list.html'


    def get(self, request):
        context = {}
        context['user'] = request.user.id
        category_list = Category.objects.all()
        context ['category_list'] = category_list
        return render(request, 'course/category_list.html',context)




def category_courses(request, slug):
    cat = Category.objects.get(slug=slug)
    courses = Course.objects.filter(category=cat.id)
    context={
        'courses':courses ,
        'title':slug,
    }
    context["user"] = request.user.id
    return render(request,'course/category_courses.html',context)



