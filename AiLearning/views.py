from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from course.models import *
from user.models import ContactUs
from publication.models import *
from django.contrib.auth.decorators import login_required

import logging

logger = logging.getLogger('ailearning')


def index(request):
    if request.method == 'GET':
        context ={}
        context["category"] = Category.objects.all()
        context["article"] = Article.objects.order_by('-date')[:5]
        context["course"] = Course.objects.order_by('-date')[:5]
        context["popular_courses"] = Course.objects.order_by('-score')[:5]
        context["popular_articles"] = Article.objects.order_by('-score')[:5]
        context["user"] = request.user.id
        return render(request, "AiLearning/index.html", context)
        

def contactus(request):
    if request.method == 'GET':
        return render(request, "AiLearning/contactus.html", {})
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        context = request.POST.get('message')
        ContactUs.objects.create(name=name,email=email,context=context)
        return HttpResponse('your message send successfuly!')




def course_rate(user, val, el_id):
    course = Course.objects.get(id=el_id)
    d = CourseRates.objects.filter(user=user,course=course).count()
    if d >= 1:
        return False
    else :
        cat = course.category
        CourseRates.objects.create(user=user,course=course)
        avg = (course.score * course.rates + int(val)) / (course.rates + 1)
        if Attend.objects.filter(user=user,course=course):
            pass
        else :
            course.add_attend()

        course.rates += 1 
        course.score = avg
        course.save()
        cat.calc_score()
            
        return True



def article_rate(user, val, el_id):
    article = Article.objects.get(id=el_id)
    d = ArticleRates.objects.filter(user=user,article=article).count()
    if d >= 1:
        return False
    else :
        ArticleRates.objects.create(user=user,article=article)
        avg = (article.score * article.rates + int(val)) / (article.rates + 1)
        article.rates += 1 
        article.score = avg
        article.save()
        return True



def prof_rate(user, val, el_id):
    prof = Professor.objects.get(id=el_id)
    d = ProfRates.objects.filter(user=user,prof=prof).count()
    if d >= 1:
        return False
    else :
        CourseRates.objects.create(user=user,prof=prof)
        avg = (prof.score * prof.rates + int(val)) / (prof.rates + 1)
        prof.rates += 1 
        prof.score = avg
        prof.save()
        return True


def lesson_rate(user ,val , el_id):
    lesson = Lesson.objects.get(id=el_id)
    d = LessonRates.objects.filter(user=user,lesson=lesson).count()
    if d >= 1:
        return False
    else :
        LessonRates.objects.create(user=user,lesson=lesson)
        avg = (lesson.score * lesson.rates + int(val)) / (lesson.rates + 1)
        lesson.rates += 1 
        lesson.score = avg
        lesson.save()
        return True



@login_required(login_url='/user/login/')
def rate(request):
    if request.method == 'POST':
        el_id = request.POST.get('el_id')
        val = request.POST.get('val')
        obj_type = str(request.POST.get('obj_type'))
        match obj_type :
            case 'course':
                if course_rate(request.user, val, el_id):
                    return JsonResponse({'success':'true'}, safe=False)
            case 'article':
                if article_rate(request.user, val, el_id):
                    return JsonResponse({'success':'true'}, safe=False)
            case 'lesson':
                if lesson_rate(request.user, val, el_id):
                    return JsonResponse({'success':'true'}, safe=False)
            case 'professor':
                if prof_rate(request.user, val, el_id):
                    return JsonResponse({'success':'true'}, safe=False)
            case _ :
              return  JsonResponse({'success':'false'})
    return  JsonResponse({'success':'false'})



