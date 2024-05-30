from django.shortcuts import render
from django.http import HttpResponse
from course.models import Category, Course
from user.models import ContactUs
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
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        context = request.POST.get('message')
        ContactUs.objects.create(name=name,email=email,context=context)
        return HttpResponse('your message send successfuly!')

