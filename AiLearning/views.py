from django.shortcuts import render

from course.models import Category, Course
from publication.models import Article



def index(request):
    if request.method == 'GET':
        context ={}
        context["category"] = Category.objects.all()
        context["course"] = Course.objects.order_by('-date')[:5]
        context["article"] = Article.objects.order_by('-date')[:5]
        context["popular_courses"] = Course.objects.order_by('-score')[:5]
        context["popular_articles"] = Article.objects.order_by('-score')[:5]
        context["user"] = request.user.id
        return render(request, "AiLearning/index.html", context)
        

def contactus(request):
    if request.method == 'GET':
        return render(request, "AiLearning/contactus.html", {})

