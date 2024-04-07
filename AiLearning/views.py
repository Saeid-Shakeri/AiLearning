from django.shortcuts import render

from course.models import Category, Course
from publication.models import Article



def index(request):
    if request.method == 'GET':
        context ={}
        context["category"] = Category.objects.all()
        context["course"] = Course.objects.order_by('-date')[:3]
        context["article"] = Article.objects.order_by('-date')[:3]
        return render(request, "AiLearning/index.html", context)
        
