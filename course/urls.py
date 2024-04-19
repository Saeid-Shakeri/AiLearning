from django.urls import path
from .views import *

app_name = "course"

urlpatterns = [
    path('courses/', CourseListView.as_view(), name='courses'),
    path('course/details/<slug:slug>/', CourseDetailView, name='course_details'),
    path('course/details/<slug:slug>/addcourse/',add_course , name='addcourse')
   

]