from django.urls import path
from . import views

urlpatterns=[
    path('',views.home,name="home"),
    path('api/register',views.register),
    path('api/getdata',views.see),
    path('api/login',views.login_view),
    path('api/userdata',views.user_view),
    path('api/logout',views.logout),
    path('register',views.register_d,name="register_d"),
    path('index',views.first_page,name="first_page"),
    ]
