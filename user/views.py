from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import update_session_auth_hash
from django.http import HttpResponse


from .models import *



def signup(request):
    message = ''
    if request.method == 'GET':
        return render(request, 'user/signup.html', {})


    elif request.method == 'POST':
        username = request.POST.get('username')
        u = User.objects.filter(username=username)
        if username in u :
            message = 'این نام کاربری موجود است لطفا یک نام دیگر را امتحان کنید.'
            return render(request,'user/signup.html',{'message':message})
        password1 = request.POST.get('password1')
        if len(str(password1)) < 8:
            message = 'رمز عبور نباید کمتر از 8 کاراکتر باشد. یک رمز دیگر بسازید.'
            return render(request,'user/signup.html',{'message':message})
        password2 = request.POST.get('password2')
        if password1 != password2 :
            message = 'رمز عبور مطابقت ندارد دوباره تلاش کنید.'
            return render(request,'user/signup.html',{'message':message})
        user = User.objects.create(username=username,password=password1)
        login(request, user)
        return redirect('user:dashboard')


        
        
    
    # return render(request, 'user/signup.html', {'form': form})


def Login(request):

    message = ''
    if request.method == 'GET':
        return render(request, 'user/login.html', {})

    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        authed_user = authenticate(
                    username=username, password=password)
        if authed_user:
            login(request, authed_user)

        # username = request.POST.get('username')
        # user = User.objects.filter(username=username)
        # if not user:
        #     message = 'نام کاربری اشتباه است. دوباره تلاش کنید.'
        #     return render(request,'user/login.html',{'message':message})

        # print(user)
        # print(username)
        # if username != user[0].username :
        #     message = 'نام کاربری اشتباه است. دوباره تلاش کنید.'
        #     return render(request,'user/login.html',{'message':message})
        # password = request.POST.get('password')
        # if  user[0].check_password(password) :
        #     message = 'رمز عبور اشتباه است. دوباره تلاش کنید'
        #     return render(request,'user/login.html',{'message':message})
        # login(request, user[0])
        return redirect('user:dashboard')


    


@login_required(login_url='/user/login/')
def Logout(request):
    logout(request)
    return redirect('user:login')


@login_required(login_url='/user/login/')
def dashboard(request):
    if request.method == 'GET':
        context ={}
        context["user"] = User.objects.get(id=request.user.id)
        return render(request, "user/dashboard.html", context)


# @login_required(login_url='/user/login/')
# def edit_profile(request):
#     if request.method == 'GET':
#         user = User.objects.get(id=request.user.id)
#         profile = EditProfile(instance = user)
#         return render(request, 'user/edit_profile.html', {'profile': profile})

#     if request.method == 'POST':
#       form = EditProfile(request.POST,instance=user)
#       if form.is_valid():
#          form.save()     
#          return redirect('dashboard')  
#       return HttpResponse("Please correct the error below.")


@login_required(login_url='/user/login/')
def change_password(request): 

    message = '' 
    if request.method == 'GET':
        return render(request, 'user/change_password.html', {})


    elif request.method == 'POST':
        oldpassword = request.POST.get('oldpassword')
        user = request.user
        if  user.check_password(oldpassword) :
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
        #3 update_session_auth_hash(request, user)
        # user.set_password(password1)
        # user.username = request.user.username
        # user.save()
        login(request, user)
        return redirect('user:dashboard')
        





        # form = PasswordChangeForm(request.user, request.POST)
    #     if form.is_valid():
    #         user = form.save()
    #         update_session_auth_hash(request, user)  # Important!
    #         return redirect('dashboard')
    #     else:
    #         HttpResponse('Please correct the error below.')
    # else:
    #     form = PasswordChangeForm(request.user)
    # return render(request, 'user/change_password.html', {'form': form})



