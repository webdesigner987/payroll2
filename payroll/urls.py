"""
URL configuration for payroll project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from payrollapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('about/', views.about, name="about"),
    path('contact/', views.contact, name="contact"),
    path('signup/', views.user_signup, name='signup'),
    path('login/', views.log_in, name='login'),
    path('setup/', views.setup, name='setup'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('people/', views.people, name='people'),
    path('logout/', views.user_logout, name='logout'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('forget-password/', views.password_reset_request, name="forget_password"),
    path('change-password/<token>/',
         views.password_reset_confirm, name="change_password"),
    path('password_reset_done/', views.password_reset_done,
         name='password_reset_done'),
    path('addone/', views.addone_employee, name='addone_employee'),
    path('step-1-sub-1/', views.step_1_sub_1, name='step_1_sub_1'),
    path('step-1-sub-2/', views.step_1_sub_2, name='step_1_sub_2'),
    path('step-1-sub-3/', views.step_1_sub_3, name='step_1_sub_3'),
    path('step-1-sub-4/', views.step_1_sub_4, name='step_1_sub_4'),
    path('success/', views.success_view, name='success_view'),
    path('step-2/', views.step_2, name='step_2'),
    path('step-3/', views.step_3, name='step_3'),
    path('mypayslips/', views.MyPaySlips, name='mypayslips'),
    path('attendance/', views.Attendance, name='attendance'),
    path('taxdeductions/', views.TaxDeduction, name='taxdeduction'),
    path('reimbursements/', views.Reimbursements, name='reimbursements'),
    path('documents/', views.Documents, name='documents'),
    path('help/', views.Help, name='help'),
    path('restrict/', views.restrict_view, name='restrict'),

]
