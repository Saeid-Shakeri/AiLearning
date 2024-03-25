from django.contrib import admin
from .models import Article
# Register your models here.



@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    exclude = ('score',)
    search_fields = ['name']

