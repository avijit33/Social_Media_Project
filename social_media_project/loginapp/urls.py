from django.urls import path
from loginapp import views

app_name = "loginapp"

urlpatterns = [
    path('signup/', views.signup, name= "signup"),
    path('login/', views.login_page, name= "login"),
    path('edit/', views.edit_profile, name= "edit"),
    path('logout/', views.logout_user, name= "logout"),
    path('profile/', views.user_profile, name= "profile"),
    path('user/<username>/', views.user, name= "user"),
    path('follow/<username>/', views.follow, name= "follow"),
    path('unfollow/<username>/', views.unfollow, name= "unfollow"),
]