from django.urls import path
from postapp import views

app_name = "postapp"

urlpatterns = [
    path('', views.home, name= "home"),
    path('liked/<pk>/', views.liked, name= "liked"),
    path('unliked/<pk>/', views.unliked, name= "unliked"),
]