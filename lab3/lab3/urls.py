"""
URL configuration for lab3 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from lab3app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.login, name="login"),
    path('adminindex/', views.admin, name="adminindex"),
    path('adminindex/adduser/', views.adduser, name="adduser"),
    path('adminindex/addlesson/', views.addlesson, name="addlesson"),
    path('adminindex/addstudy/', views.addstudy, name="addstudy"),
    path('student/', views.student, name="studentindex"),
    path('teacher/', views.teacher, name="teacherindex"),
    path('teacher/lesson', views.lesson, name="lesson"),
    path('teacher/editscore', views.editscore, name="editscore")


]

