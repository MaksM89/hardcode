from django.shortcuts import get_object_or_404

# Create your views here.
from django.http import HttpResponse
from .models import *
from datetime import time, date, timedelta
from json import dumps

def get_lessons(request, user_id, product_id=None):
    user = get_object_or_404(Students, id=user_id)
    if product_id is None:
        lessons = user.products.values('lessons__id').distinct()
    else:
        lessons = user.products.filter(id=product_id).values('lessons__id').distinct()
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

def get_stats(request):
    answer = {}
    for product in Products.objects.all():
        completed_id = set()
        totaltime = timedelta(seconds=0)
        for h in StudentHistory.objects.filter(lesson__in=product.lessons.distinct()).all():
            if h.complete:
                completed_id.add(h.lesson.id)
            totaltime += timedelta(hours=h.viewed.hour, minutes=h.viewed.minute, seconds=h.viewed.second)
        hours = totaltime.seconds // 3600
        minutes = (totaltime.seconds - (hours * 3600)) // 60
        seconds = totaltime.seconds  - (hours * 3600) - minutes * 60
        hours += totaltime.days * 24
        users_count = product.students_set.count()
        total_users = Students.objects.count()
        answer[product.name] = {
            'viewed_lections': len(completed_id),
            'total_time_viewed': f'{hours}:{minutes:02}:{seconds:02}',
            'total_students': users_count,
            'buying_percentage': f'{users_count / total_users:.2%}'
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

