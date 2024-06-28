from django.contrib import admin
from .models import Lesson, Category, Course, LessonComment, CourseComment, Professor
# Register your models here.


class InlineLesson(admin.StackedInline):
    model = Lesson
    extra = 0
    exclude = ('score','rates','attends','date')


class CourseCommentInline(admin.StackedInline):
    model = CourseComment
    extra = 0
    exclude = ('likes','dislikes',)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    inlines = [InlineLesson,CourseCommentInline] 
    exclude = ('score','rates','attends','date',)
    search_fields = ['name']


@admin.register(CourseComment)
class CourseComment(admin.ModelAdmin):
    exclude = ('likes','dislikes',)
    search_fields = ['name']




class LessonCommentInline(admin.StackedInline):
    model = LessonComment
    extra = 0
    exclude = ('likes','dislikes',)



@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    inlines = [LessonCommentInline] 
    exclude = ('score','rates','date')
    search_fields = ['name']


@admin.register(LessonComment)
class LessonComment(admin.ModelAdmin):
    exclude = ('likes','dislikes',)
    search_fields = ['name']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    exclude = ('score','rates')
    search_fields = ['name']


@admin.register(Professor)
class ProfessorAdmin(admin.ModelAdmin):
    exclude = ('score','rates',)
    ordering = ['name']
    search_fields = ['name']