from django.urls import path
from . import views

urlpatterns = [
    path('', views.note_list, name='note_list'),
    path('notes/create/', views.note_create, name='note_create'),
    path('health/', views.health_check, name='health_check'),
]
