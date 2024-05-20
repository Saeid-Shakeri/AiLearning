from django.urls import path
from .views import *



urlpatterns = [
    path('articles/', ArticleListView.as_view(), name='article_list'),
    path('article/details/<slug:slug>/', ArticleDetailView.as_view(), name='article_details'),
   

]