from django.shortcuts import render
from django.views.generic import ListView, View, DetailView
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
# from django.http impor


from .models import *
from publication.models import Article
# from user.models import Attend


class CourseListView(ListView):
    # model = Course
    # context_object_name = 'course_list'
    # queryset = Course.objects.order_by('-date')
    # template_name = 'course/course_list.html'
    # # paginate_by = 5

    def get(self, request):
        context = {}
        context['user'] = request.user.id
        course_list = Course.objects.order_by('-date')
        context ['course_list'] = course_list
        return render(request,'course/course_list.html',context)




    
def CourseDetailView(request, slug):
    course = Course.objects.get(slug=slug)
    prof = course.professor.all()
    lessons = Lesson.objects.filter(course=course.id)

    context={
        'course': course, 'prof': prof, 'lessons': lessons, 
    }
    context["user"] = request.user.id
    return render(request,'course/course_detail.html',context)


@login_required(login_url='/user/login/')
def add_course(request, **kwargs):
    user = request.user
    course_id = request.POST['course_id']
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
    queryset = Category.objects.all()
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
        'title':slug
    }
    context["user"] = request.user.id
    return render(request,'course/category_courses.html',context)


def lesson(request, slug):
    lesson = Lesson.objects.get(slug=slug)
    context = {
        'lesson' : lesson

       }
    context["user"] = request.user.id
    return render(request,'course/lesson.html',context)


@login_required(login_url='/user/login/')
def rate_course(request):
    if request.method == 'POST':
        element_id = request.POST.get('el_id')
        val = request.POST.get('val')
        course = Course.objects.get(id=element_id)
        d = CourseRates.objects.filter(user=request.user,course=course).count()
        if d >= 1:
            return JsonResponse({'success':'false',})
        else :
            CourseRates.objects.create(user=request.user,course=course)
            course.rates += 1 
            course.save()
            avg = (course.score * course.rates + int(val)) / course.rates 
            course.score = avg
            course.save()
            return JsonResponse({'success':'true'}, safe=False)
    return JsonResponse({'success':'false'})