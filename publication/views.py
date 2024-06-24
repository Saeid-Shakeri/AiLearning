from django.shortcuts import render
from django.views.generic import ListView, View
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import *

# Create your views here.

class ArticleListView(ListView):
    model = Article
    
    #paginate_by = 5
    def get(self, request):
        context = {}
        context ['user'] = request.user.id
        article_list = Article.objects.order_by('-date')
        popular_article = Article.objects.order_by('-score')

        context ['article_list'] = article_list
        context ['popular_article'] = popular_article
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
        context["comments"] = ArticleComment.objects.filter(article=article,checked=True).order_by('-id')

        return render(request,'publication/article_detail.html',context)
    

    def post(self, request, slug):
        name = request.POST.get('name')
        email = request.POST.get('email')
        comment = request.POST.get('comment')
        article = Article.objects.get(slug=slug)
        ArticleComment.objects.create(name=name,email=email,content=comment,article=article)
        prof = article.author.all()
        comments = ArticleComment.objects.filter(article=article,checked=True).order_by('-id')

        context={
            'article':article, 'prof': prof, 'comments':comments,
        }
        context["user"] = request.user.id
        context["rate"] = ArticleRates.objects.filter(user=request.user.id,article=article)
        return render(request,'publication/article_detail.html',context)




@login_required(login_url='/user/login/')
def like_articlecomment(request,id):
    comment = ArticleComment.objects.get(id=id)
    if not comment.likes.filter(id=request.user.id).exists():
        comment.likes.add(request.user)
        if comment.dislikes.filter(id=request.user.id).exists():
            comment.dislikes.remove(request.user)
    slug = comment.article.slug
    return HttpResponseRedirect(reverse('article_details', args=[slug]))


@login_required(login_url='/user/login/')
def dislike_articlecomment(request, id):
    comment = ArticleComment.objects.get(id=id)
    if not comment.dislikes.filter(id=request.user.id).exists():
        comment.dislikes.add(request.user)
        if comment.likes.filter(id=request.user.id).exists():
            comment.likes.remove(request.user)
    slug = comment.article.slug
    return HttpResponseRedirect(reverse('article_details', args=[slug]))
