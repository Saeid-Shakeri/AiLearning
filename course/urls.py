from django.urls import path

urlpatterns = [
    path('',  , name='landing'),
    path('courses/',       , name='courses'),
    path('course/details/<slug:slug>/',       , name='course_details'),
   

]