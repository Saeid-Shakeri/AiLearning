from django.urls import path
from .views import *

urlpatterns = [
    path('signup/', signup, name='singup'),
    path('login/', Login, name='login'),
    path('logout/', Logout, name='logout'),
    # path('restore/',          , name='restore'),
    path('dashboard/', dashboard, name='dashboard'),
    path('dashboard/profile/', edit_profile, name='edot_profile'),
    path('dashboard/password/', change_password, name='change_password'),
    # path('dashboard/courses/',      , name='corses'),


]
