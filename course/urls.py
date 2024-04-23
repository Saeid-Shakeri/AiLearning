from django.urls import path
from .views import *

app_name = "course"

urlpatterns = [
    path('courses/', CourseListView.as_view(), name='courses'),
    path('details/<slug:slug>/', CourseDetailView, name='course_details'),
    path('details/<slug:slug>/addcourse/',add_course , name='addcourse'),
    path('categories/<slug:slug>/', category_courses, name='category_courses'),
    path('categories/', CategoryListView.as_view(), name='category_list'),
    path('lesson/<slug:slug>/', lesson, name='lesson')

   

]