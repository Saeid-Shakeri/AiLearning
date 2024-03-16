from django.contrib import admin
from .models import Course, Lesson, Category, Professor
# Register your models here.

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    exclude = ('score')

@admin.register(Lesson)
class CourseAdmin(admin.ModelAdmin):
    exclude = ('score')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    exclude = ('score',)


@admin.register(Professor)
class ProfessorAdmin(admin.ModelAdmin):
    
    exclude = ('score',)
