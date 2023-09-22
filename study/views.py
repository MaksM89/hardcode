from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.http import HttpResponse
from .models import *
from datetime import time, date, timedelta
from json import dumps


def index(request):
    return HttpResponse("Hello, world!")

def get_lessons(request, user_id):
    user = get_object_or_404(Students, id=user_id)
    lessons = user.products.values('lessons__id').distinct()
    history = StudentHistory.objects.filter(student=user, lesson__in=lessons)
    answer = {
        'user': {
            'name': user.name,
            'surname': user.surname
        },
        'lessons':
            [
                {
                    'title': h.lesson.title,
                    'last_viewed_date': str(h.lastdate),
                    'viewed': str(h.viewed),
                    'completed': h.complete
                }
                for h in history
            ]
    }
    return HttpResponse(dumps(answer))

def init_db(request):
    Students.objects.all().delete()
    Products.objects.all().delete()
    Lessons.objects.all().delete()

    user1 = Students(name='Petya', surname='P')
    user2 = Students(name='Vasya', surname='V')
    user1.save()
    user2.save()

    python = Products(name='python')
    java = Products(name='java')
    python.save()
    java.save()

    l1 = Lessons(title='intro', videolink='1.avi', duration=time(0, 1, 30))
    lp2 = Lessons(title='course', videolink='2p.avi', duration=time(1, 30, 0))
    lj2 = Lessons(title='course', videolink='2j.avi', duration=time(1, 30, 0))
    l3 = Lessons(title='outro', videolink='3.avi', duration=time(0, 1, 30))
    l1.save();lp2.save();lj2.save();l3.save()

    python.lessons.set((l1, lp2, l3))
    java.lessons.set((l1, lj2, l3))

    user1.products.set((python, java))
    user2.products.add(java)

    StudentHistory(
        student=user1,
        lesson=l1,
        lastdate=date.today() - timedelta(days=1),
        viewed=time(0, 0, 5)
    ).save()
    StudentHistory(
        student=user1,
        lesson=l1,
        viewed=l1.duration
    ).save()
    StudentHistory(
        student=user1,
        lesson=lp2,
        viewed=time(1, 25, 0)
    ).save()
    StudentHistory(
        student=user1,
        lesson=lj2,
        viewed=time(0, 25, 0)
    ).save()
    StudentHistory(
        student=user2,
        lesson=l1,
        viewed=l1.duration
    ).save()
    StudentHistory(
        student=user2,
        lesson=lj2,
        viewed=time(0, 25, 0)
    ).save()
    d = '<p>'.join(str(x) for x in StudentHistory.objects.all())
    return HttpResponse(d)

