from django.urls import path
from . import views

urlpatterns = [
    path('all_users/', views.all_users),
]