from django.urls import path
from . import views

urlpatterns =[
     path('login',view=views.Login.as_view(),name='login'),
     path('createUser',view=views.CreateUser.as_view(),name='createUser'),
     path('logout',view=views.Logout.as_view(),name='logout')
]