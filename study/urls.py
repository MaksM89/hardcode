from django.urls import path

from . import views

urlpatterns = [
    path('init', views.init_db, name='init_db'),
    path('user/<int:user_id>', views.get_lessons, name='task1'),
    path('user/<int:user_id>/<int:product_id>', views.get_lessons, name='task2'),
    path('stats', views.get_stats, name='task3')
]