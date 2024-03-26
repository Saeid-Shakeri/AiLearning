from django.shortcuts import render
from django.views.generic import ListView, View

from .models import Article


# Create your views here.
class ArticleListView(ListView):
    model = Article
    context_object_name = 'article_list'
    queryset = Article.objects.order_by('-date')
    template_name = 'publication/article_list.html'
    #paginate_by = 5


class ArticleDetailView(View):
    
    def get(self, request, slug):
        article = Article.objects.get(slug=slug)
        prof = article.author.all()
        context={
            'article':article, 'prof': prof
        }
        return render(request,'publication/article_detail.html',context)


    