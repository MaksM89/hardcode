from django.db import models
from datetime import date

# Create your models here.

# class Owner(models.Model):
#     name = models.TextField()
#     surname = models.TextField()

class Lessons(models.Model):
    title = models.TextField()
    videolink = models.FilePathField()
    duration = models.TimeField()

    def __str__(self):
        return f'L <{self.title}, {self.videolink}, {self.duration}>'

class Products(models.Model):
    # owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
    name = models.TextField()
    lessons = models.ManyToManyField(Lessons)

    def __str__(self):
        return f'P <{self.name}>'

class Students(models.Model):
    name = models.TextField()
    surname = models.TextField()
    products = models.ManyToManyField(Products)

    def __str__(self):
        return f'S <{self.name}, {self.surname}>'

class StudentHistory(models.Model):
    student = models.ForeignKey(Students, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lessons, on_delete=models.CASCADE)
    lastdate = models.DateField(default=date.today())
    viewed = models.TimeField()

    @property
    def complete(self):
        sec_v = self.viewed.hour * 3600 + self.viewed.minute * 60 + self.viewed.second
        sec_l = self.lesson.duration.hour * 3600 + self.lesson.duration.minute * 60 +\
                   self.lesson.duration.second
        return (sec_v / sec_l) >= 0.8

    def __str__(self):
        return f'H <{self.student.name}, {self.lesson.title}, {self.lastdate}, {self.complete}>'
