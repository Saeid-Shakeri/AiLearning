from django.urls import path
from .views import *



urlpatterns = [
    path('articles/', ArticleListView.as_view(), name='article_list'),
    path('article/details/<slug:slug>/', ArticleDetailView.as_view(), name='article_details'),
    path('like_articlecomment/<int:id>/',like_articlecomment, name='like_articlecomment'),
    path('dislike_articlecomment/<int:id>/',dislike_articlecomment,  name='dislike_articlecomment'),


   

]