from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.http import HttpResponse


from .forms import *
from .models import *



def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = SignupForm()
    return render(request, 'user/signup.html', {'form': form})


def Login(request):
    form = LoginForm()
    message = ''
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                return redirect('dashboard')
        message = 'Login failed!'
    return render(request, 'user/login.html', context={'form': form, 'message': message})


@login_required(login_url='/user/login')
def Logout(request):
    logout(request)
    return redirect('login')


@login_required(login_url='/user/login')
def dashboard(request):
    if request.method == 'GET':
        context ={}
        context["user"] = User.objects.filter(id=request.user.id)
        return render(request, "user/dashboard.html", context)


@login_required(login_url='/user/login')
def edit_profile(request):
    if request.method == 'GET':
        user = User.objects.get(id=request.user.id)
        profile = EditProfile(instance = user)
        return render(request, 'user/edit_profile.html', {'profile': profile})

    if request.method == 'POST':
      form = EditProfile(request.POST,instance=user)
      if form.is_valid():
         form.save()     
         return redirect('dashboard')  
      return HttpResponse("Something went wrong")


@login_required(login_url='/user/login')
def change_password(request):  
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            return redirect('dashboard')
        else:
            HttpResponse('Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'user/change_password.html', {'form': form})






    