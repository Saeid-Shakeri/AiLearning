from django.shortcuts import render
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
