from django.shortcuts import render
from django.views.generic import ListView,DetailView

from .models import Course, Category
from publication.models import Article
# Create your views here.

def IndexView(request):
    if request.method == 'GET':
        context ={}
        context["category"] = Category.objects.all()
        context["course"] = Course.objects.order_by('-date')[:3]
        context["article"] = Article.objects.order_by('-date')[:3]
        return render(request, "course/index.html", context)


class CourseListView(ListView):
    model = Course
    context_object_name = 'course_list'
    queryset = Course.objects.order_by('-date')
    template_name = 'course/course_list.html'
    #paginate_by = 5



class CourseDetailView(DetailView):
    model = Course
    template_name = "course/course_detail.html"



