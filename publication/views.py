from django.shortcuts import render
from django.views.generic import ListView, View

from .models import Article


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
        prof = article.author.all()
        context={
            'article':article, 'prof': prof
        }
        context["user"] = request.user.id

        return render(request,'publication/article_detail.html',context)


    