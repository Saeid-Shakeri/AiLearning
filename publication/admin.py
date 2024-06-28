from django.contrib import admin
from .models import Article, ArticleComment
# Register your models here.

class ArticleCommentInline(admin.StackedInline):
    model = ArticleComment
    extra = 0
    exclude = ('likes','dislikes',)

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    inlines = [ArticleCommentInline] 
    exclude = ('score','readers','rates','date')
    search_fields = ['name']


@admin.register(ArticleComment)
class ArticleCommentAdmin(admin.ModelAdmin):
    exclude = ('likes','dislikes',)
    search_fields = ['name']

