from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
import logging

from .models import *
from course.models import Attend,Course,Category

logger = logging.getLogger('user')



def signup(request):
    message = ''
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect("index")
        return render(request, 'user/signup_login.html', {'user':request.user.id})


    elif request.method == 'POST':
        try : 
            username = request.POST.get('username')
            u = User.objects.filter(username=username)
            for i in u:
                if username == i.username:
                    message = 'این نام کاربری موجود است لطفا یک نام دیگر را امتحان کنید.'
                    return render(request,'user/signup_login.html',{'message':message,'user':request.user.id})
            email = request.POST.get('email')
            u = User.objects.filter(email=email)
            for i in u :
                if email == i.email :
                    message = 'این ایمیل موجود است لطفا یک ایمیل دیگر را امتحان کنید.'
                    return render(request,'user/signup_login.html',{'message':message,'user':request.user.id})
            password1 = request.POST.get('password1')
            # if len(str(password1)) < 8:
            #     message = 'رمز عبور نباید کمتر از 8 کاراکتر باشد. یک رمز دیگر بسازید.'
            #     return render(request,'user/signup_login.html',{'message':message,'user':request.user.id})
            password2 = request.POST.get('password2')
            if password1 != password2 :
                message = 'رمز عبور مطابقت ندارد دوباره تلاش کنید.'
                return render(request,'user/signup_login.html',{'message':message,'user':request.user.id})
            user = User.objects.create(username=username,email=email)
            user.set_password(password1)
            user.save()
            login(request, user)
            return redirect('dashboard')
        except Exception as e:
            message = 'A problem occurred. please try again later'
            logger.warning(f'signup view: {str(e)}')
            return render(request,'user/signup_login.html',{'message':message,'user':request.user.id})



def Login(request):

    message = ''
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect("index")
        return render(request, 'user/signup_login.html', {'user':request.user.id})

    elif request.method == 'POST':
        try: 
            email_username = request.POST.get('email_username')
            password = request.POST.get('password')

            authed_user = authenticate(
                        username=email_username, password=password)
            if authed_user:
                login(request, authed_user)
                return redirect('dashboard')
            u = User.objects.filter(email=email_username)
            authed_user = authenticate(
                        username=u[0].username, password=password)
            if authed_user:
                login(request, authed_user)
                return redirect('dashboard')
            else :
                message = 'رمز عبور یا نام کاربری اشتباه است. دوباره تلاش کنید'
                return render(request,'user/signup_login.html',{'message':message, 'user':request.user.id})
        except Exception as e:
            message = 'A problem occurred. please try again later'
            logger.warning(f'Login view: {str(e)}')
            return render(request,'user/signup_login.html',{'message':message,'user':request.user.id})



@login_required(login_url='/user/login/')
def Logout(request):
    logout(request)
    return redirect('login')


@login_required(login_url='/user/login/')
def dashboard(request):
    if request.method == 'GET':
        context ={}
        context["user"] = User.objects.get(id=request.user.id)
        context ["attended"] = Attend.objects.filter(user=request.user)
        # course.id = Course.objects.filter()
        # context ['similar'] = Category.objects.filter(id=)
        # if context ["attended"]:
        # print(context["attended"])
        # context["attend"] = Attend.objects.filter(user=request.user.id)

        return render(request, "user/dashboard.html", context)



@login_required(login_url='/user/login/')
def edit_profile(request):
   
    user = request.user

    if request.method == 'GET':
        return render(request, 'user/edit_profile.html', {'user':user})

    if request.method == 'POST':
        try: 
            username = request.POST.get('username')
            u = User.objects.filter(username=username)
            if username in u :
                message = 'این نام کاربری موجود است لطفا یک نام دیگر را امتحان کنید.'
                return render(request,'user/edit_profile.html',{'message':message}) 
            else :
                user.username = username
            if user.first_name !=  request.POST.get("first_name"):
                user.first_name = request.POST.get("first_name")
            if user.last_name != request.POST.get("last_name"):
                user.last_name = request.POST.get("last_name")
            if user.phone !=  request.POST.get("phone"):
                user.phone = request.POST.get("phone")
            if user.email !=  request.POST.get("email"):
                user.email = request.POST.get("email")
            
            user.save()
            return redirect('dashboard')  
        except Exception as e:
            message = 'A problem occurred. please try again later'
            logger.warning(f'edit_profile view: {str(e)}')
            return render(request,'user/edit_profile.html',{'message':message,'user':request.user.id})




@login_required(login_url='/user/login/')
def change_password(request): 

    message = '' 
    if request.method == 'GET':
        return render(request, 'user/change_password.html', {})


    elif request.method == 'POST':
        try:
            oldpassword = request.POST.get('oldpassword')
            user = request.user
            if  not user.check_password(oldpassword) :
                message = 'رمز قبلی را اشتباه نوشته اید. دوباره تلاش کنید. '
                return render(request,'user/change_password.html',{'message':message})
            password1 = request.POST.get('password1')
            if len(str(password1)) < 8:
                message = 'رمز عبور نباید کمتر از 8 کاراکتر باشد. یک رمز دیگر بسازید.'
                return render(request,'user/change_password.html',{'message':message})
            password2 = request.POST.get('password2')
            if password1 != password2 :
                message = 'رمز عبور جدید مطابقت ندارد دوباره تلاش کنید.'
                return render(request,'user/change_password.html',{'message':message})
            user.set_password(password1)
            user.save()
            login(request, user)
            return redirect('dashboard')
        except Exception as e:
            message = 'A problem occurred. please try again later'
            logger.warning(f'change_password view: {str(e)}')
            return render(request,'user/change_password.html',{'message':message,'user':request.user.id})


@login_required(login_url='/user/login/')
def resetpass(request):
    pass