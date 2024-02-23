from django.db import models

# Create your models here.
class Role(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Users(models.Model):
    username = models.CharField(max_length=100)
    password = models.TextField()
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.username
    
class Lesson(models.Model):
    title = models.CharField(max_length=200)
    teacher = models.ForeignKey(Users, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Study(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    score = models.IntegerField()

    def __str__(self):
        return f"{self.user.username} - {self.lesson.title}"