from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('init', views.init_db, name='init_db'),
    path('user/<int:user_id>', views.get_lessons, name='init_db')
]