from django.shortcuts import render
from django.views.generic import ListView, View

from .models import Course, Category
from publication.models import Article
# Create your views here.


class CourseListView(ListView):
    model = Course
    context_object_name = 'course_list'
    queryset = Course.objects.order_by('-date')
    template_name = 'course/course_list.html'
    #paginate_by = 5



class CourseDetailView(View):
    
    def get(self, request, slug):
        course = Course.objects.get(slug=slug)
        prof = course.professor.all()
        context={
            'course':course, 'prof': prof
        }
        return render(request,'course/course_detail.html',context)


    