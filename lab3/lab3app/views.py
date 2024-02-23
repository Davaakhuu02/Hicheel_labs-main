from django.shortcuts import render, redirect
from django.contrib import messages 
from django.contrib.sessions.models import Session
from .models import *
from django.db.models import Q

# Create your views here.

def login(request):
    if request.session.get('roleid'):
         if request.session.get('roleid') == 1:
            return redirect('adminindex')
         elif request.session.get('roleid') == 2:
             return redirect('studentindex')
         elif request.session.get('roleid') == 3:
             return redirect('teacherindex')
    else:
        if request.method == "POST":
            username = request.POST.get('uname')
            password = request.POST.get('psw')
            try:
                user = Users.objects.get(username=username, password=password)
                if user: 
                    request.session['userid'] = user.id 
                    request.session['roleid'] = user.role.id
                    if user.role.id == 1 :
                        return redirect("adminindex")
                    elif user.role.id == 2 :
                        return redirect("studentindex")
                    elif user.role.id == 3 :
                        return redirect("teacherindex")
                # Authentication successful, proceed with further actions
            except Users.DoesNotExist:
                # Authentication failed, handle accordingly
                print("User not found or invalid password")
                return redirect('login')
        else:
            return render(request, "login.html")

def admin(request):
    if request.session.get('roleid'):
        if request.session.get('roleid') == 2:
             return redirect('studentindex')
        elif request.session.get('roleid') == 3:
             return redirect('teacherindex')
        else:
            if request.method == "POST":
                if request.POST.get('logout'):
                    request.session.flush()
                    return redirect('login')
            else:
                users = Users.objects.all()
                lessons = Lesson.objects.all()
                study = Study.objects.all()
                context = {
                    "users":users,
                    "lessons":lessons,
                    "studys":study,
                }
                return render(request, "admin/index.html", context=context)
    else:
         return redirect('login')


def adduser(request):
    if request.session.get('roleid'):
        if request.session.get('roleid') == 2:
             return redirect('studentindex')
        elif request.session.get('roleid') == 3:
             return redirect('teacherindex')
        else:
            if request.method == "POST":
                username = request.POST.get('username')
                password = request.POST.get('password')
                role_id = request.POST.get('role')
                
                role = Role.objects.get(id=role_id)
                user_test = Users.objects.filter(username = username, password = password, role_id=role_id)
                if user_test:
                    messages.error(request, 'User already exists.')
                    return redirect('adduser')
                else:
                    user = Users.objects.create(username=username, password=password, role=role)
                    user.save()
                    
                    return redirect('adminindex')
            else:
                roles = Role.objects.all()
                return render(request, "admin/adduser.html", context= {"roles":roles})
    else:
        return redirect('login')

def addlesson(request):
    if request.session.get('roleid'):
        if request.session.get('roleid') == 2:
             return redirect('studentindex')
        elif request.session.get('roleid') == 3:
             return redirect('teacherindex')
        else:
            if request.method == "POST":
                title = request.POST.get('title')
                teacherid = request.POST.get('teacherid')
                lesson_test = Lesson.objects.filter(title = title, teacher = teacherid)
                if lesson_test:
                            messages.error(request, 'Lesson already exists.')
                            return redirect('addlesson')
                else:
                    lesson = Lesson.objects.create(title=title, teacher_id=teacherid)
                    lesson.save()
                
                    return redirect('adminindex')
            else:
                teachers = Users.objects.filter(role_id = 3)
                return render(request, "admin/addlesson.html", context= {"teachers":teachers})
    else:
        return redirect('login')
    
def addstudy(request):
    if request.session.get('roleid'):
        if request.session.get('roleid') == 2:
             return redirect('studentindex')
        elif request.session.get('roleid') == 3:
             return redirect('teacherindex')
        else:
            if request.method == "POST":
                userid = request.POST.get('userid')
                lessonid = request.POST.get('lessonid')
                
                user = Users.objects.get(id=userid)
                lesson = Lesson.objects.get(id=lessonid)
                study_test = Study.objects.filter(user = userid, lesson = lessonid)
                if study_test:
                            messages.error(request, 'Study already exists.')
                            return redirect('addstudy')
                else:
                    study = Study.objects.create(user=user, lesson=lesson, score=0)
                    study.save()
                    
                    return redirect('adminindex')
            else:
                users = Users.objects.filter(role_id = 2)
                lessons = Lesson.objects.all()

                return render(request, "admin/addstudy.html", context= {"users":users, "lessons":lessons})
    else:
        return redirect('login')

def student(request):
    if request.session.get('roleid'):
        if request.session.get('roleid') == 1:
             return redirect('adminindex')
        elif request.session.get('roleid') == 3:
             return redirect('teacherindex')
        else:
            if request.method == "POST":
                if request.POST.get('logout'):
                    request.session.flush()
                    return redirect('login')
            else:
                my_lessons = Study.objects.filter(user = request.session.get('userid'))
                context = {"my_lessons": my_lessons}
                return render(request, "student/index.html", context)
    else:
        return redirect('login')
def teacher(request):
    if request.session.get('roleid'):
        if request.session.get('roleid') == 2:
             return redirect('studentindex')
        elif request.session.get('roleid') == 1:
             return redirect('adminindex')
        else:
            if request.method == "POST":
                if request.POST.get('logout'):
                    request.session.flush()
                    return redirect('login')
            else:
                lessons = Lesson.objects.filter(teacher = 3)
                context = {
                    "lessons":lessons
                }
                return render(request, "teacher/index.html",context)
    else:
        return redirect('login')
    
def lesson(request):  
        id = request.GET.get('lessonid')
        lesson = Lesson.objects.get(id = id)
        users = Study.objects.filter(lesson=id)
        context = {"id":id,
                "users":users,
                "lesson":lesson,}
        return render(request, "teacher/lesson.html", context)
def editscore(request):  
        if request.method == "POST":
             lessonid = request.POST.get('lessonid')
             studyid = request.POST.get('studyid')
             score = request.POST.get('score')
             study = Study.objects.get(id = studyid)
             study.score = int(score)
             study.save()
             return redirect(f'http://127.0.0.1:8000/teacher/lesson?lessonid={lessonid}')
        else:
            lessonid = request.GET.get('lessonid')
            userid = request.GET.get('userid')
            study = Study.objects.get(id = userid)
            
            context = {
                    "study":study,}
            return render(request, "teacher/editscore.html", context)
