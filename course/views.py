from django.shortcuts import render
from django.views.generic import ListView, View, DetailView
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse


from .models import Course, Category
from publication.models import Article
from user.models import Attend


class CourseListView(ListView):
    model = Course
    context_object_name = 'course_list'
    queryset = Course.objects.order_by('-date')
    template_name = 'course/course_list.html'
    # paginate_by = 5



    
def CourseDetailView(request, slug):
    course = Course.objects.get(slug=slug)
    prof = course.professor.all()
    context={
        'course':course, 'prof': prof
    }
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
    return HttpResponse('the course added to your profile')
        

class CategoryListView(ListView):
    pass


class CategoryDetailView(DetailView):
    pass
