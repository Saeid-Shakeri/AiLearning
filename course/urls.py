from django.urls import path
from .views import *

urlpatterns = [
    path('', IndexView , name='landing'),
    path('courses/', CourseListView.as_view(), name='courses'),
    #path('course/details/<slug:slug>/',       , name='course_details'),
   

]