from django.urls import path
from .views import *


urlpatterns = [
    path('courses/', CourseListView.as_view(), name='courses'),
    path('details/<slug:slug>/', CourseDetailView, name='course_details'),
    path('details/<slug:slug>/addcourse/',add_course , name='addcourse'),
    path('details/<slug:slug>/continue_course/', continue_course, name='continue_course'),
    path('categories/<slug:slug>/', category_courses, name='category_courses'),
    path('categories/', CategoryListView.as_view(), name='category_list'),
    path('lesson/<slug:slug>/', get_lesson, name='get_lesson'),
    path('like_coursecomment/<int:id>/',like_coursecomment,name="like_coursecomment"),
    path('dislike_coursecomment/<int:id>/',dislike_coursecomment,name="dislike_coursecomment"),
    path('like_lessoncomment/<int:id>/',like_lessoncomment,name="like_lessoncomment"),
    path('dislike_lessoncomment/<int:id>/',dislike_lessoncomment,name="dislike_lessoncomment"),

]