from . import views
from django.urls import path

urlpatterns = [
    #Account
    path('login/', views.signin, name='login'),
    path('logout/', views.loggingout, name='logout'),
    path('register/', views.Register, name='register'),

    #Home
    path('', views.index, name='home'),
]