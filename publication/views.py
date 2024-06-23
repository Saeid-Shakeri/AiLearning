from django.shortcuts import render
from django.views.generic import ListView, View
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from .models import *


# Create your views here.
class ArticleListView(ListView):
    model = Article
    
    #paginate_by = 5
    def get(self, request):
        context = {}
        context ['user'] = request.user.id
        article_list = Article.objects.order_by('-date')
        context ['article_list'] = article_list
        return render(request,'publication/article_list.html',context)



class ArticleDetailView(View):
    
    def get(self, request, slug):
        article = Article.objects.get(slug=slug)
        article.readers +=1
        article.save()
        prof = article.author.all()
        context={
            'article':article, 'prof': prof
        }
        context["user"] = request.user.id
        context["rate"] = ArticleRates.objects.filter(user=request.user.id,article=article)
        return render(request,'publication/article_detail.html',context)
    

    def post(self, request, slug):
        name = request.POST.get('name')
        email = request.POST.get('email')
        comment = request.POST.get('comment')
        ArticleComment.objects.create(name=name,email=email,content=comment,article=self)
        prof = self.author.all()
        comments = ArticleComment.objects.filter(article=self).order_by('-id')

        context={
            'article':self, 'prof': prof, 'comments':comments,
        }
        context["user"] = request.user.id
        context["rate"] = ArticleRates.objects.filter(user=request.user.id,article=self)
        return render(request,'publication/article_detail.html',context)

