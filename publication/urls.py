from django.urls import path
from .views import *

urlpatterns = [
    path('publications/', ArticleListView.as_view(), name='article_lisr'),
    path('publication/details/<slug:slug>/', ArticleDetailView.as_view(), name='article_details'),
   

]