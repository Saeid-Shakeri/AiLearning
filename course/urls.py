from django.urls import path
from .views import *

urlpatterns = [
    path('courses/', CourseListView.as_view(), name='courses'),
    path('course/details/<slug:slug>/', CourseDetailView.as_view(), name='course_details'),
   

]