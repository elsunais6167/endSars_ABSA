from  . import views
from django.urls import path

urlpatterns = [
    #Account
    path('login/', views.signin, name='login'),
    path('logout/', views.loggingout, name='logout'),
    path('register/', views.Register, name='register'),

    #Non-Login Pages
    path('', views.index, name='home'),
    path('knowledge-hub', views.hub, name='knowledge-hub'),
    path('report-list', views.reports_list, name='report-list'),

    #Admin
    path('admin-dashboard', views.admin_dasboard, name='admin-dashboard'),
    path('admin-reports', views.admin_reports, name='admin-reports'),
    path('admin-hub', views.admin_hub, name='admin-hub'),
    path('admin-users', views.admin_users, name='admin-users'),

    #generic
    path('content/<str:pk>/', views.content, name='content')
]