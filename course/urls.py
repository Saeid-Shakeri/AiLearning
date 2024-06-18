from django.urls import path
from .views import *


urlpatterns = [
    path('courses/', CourseListView.as_view(), name='courses'),
    path('details/<slug:slug>/', CourseDetailView, name='course_details'),
    path('details/<slug:slug>/addcourse/',add_course , name='addcourse'),
    path('details/<slug:slug>/continue-course/', continue_course, name='continue_course'),
    path('categories/<slug:slug>/', category_courses, name='category_courses'),
    path('categories/', CategoryListView.as_view(), name='category_list'),
    path('lesson/<slug:slug>/', lesson, name='lesson'),

]