# payrollapp/admin.py
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin
from .models import Employee
from django.contrib import admin
from .models import *


@admin.register(Step1Sub1)
class Step1Sub1Admin(admin.ModelAdmin):
    list_display = ('id', 'user', 'company_gstin')


@admin.register(Step1Sub2)
class Step1Sub2Admin(admin.ModelAdmin):
    list_display = ('id', 'user', 'organization_type', 'company_pan')


@admin.register(Step1Sub3)
class Step1Sub3Admin(admin.ModelAdmin):
    list_display = ('id', 'brand_name', 'get_user',
                    'work_address', 'pincode', 'state')

    def get_user(self, obj):
        return obj.user.username

    get_user.short_description = 'User'


@admin.register(Step1Sub4)
class Step1Sub4Admin(admin.ModelAdmin):
    list_display = ('id', 'user', 'brand_name', 'organization_type', 'company_gstin',
                    'company_pan', 'company_name', 'registered_address', 'pincode', 'state')


@admin.register(Step2)
class Step2Admin(admin.ModelAdmin):
    list_display = ('id', 'user', 'payroll_enabled', 'payroll_date',
                    'auto_run_payroll', 'employee_request_advance')


@admin.register(Step3)
class Step3Admin(admin.ModelAdmin):
    list_display = ('id', 'user', 'use_default_salary_structure',
                    'if_good_description', 'consider_fbp')


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'first_login')


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'employee_type', 'hire_date', 'job_title', 'department', 'manager',
                    'annual_salary', 'location', 'resident_of_india', 'pan_number', 'ifsc_code', 'account_number', 'beneficiary_name',
                    'pf_status', 'provident_fund_uan', 'pf_wages_calculation', 'include_employer_contribution', 'contribute_to_pf_eps',
                    'pt_status', 'pt_location']


# In your admin.py file


# Unregister the default UserAdmin
admin.site.unregister(User)


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff',
         'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )


# Register your custom Group model if applicable
admin.site.unregister(Group)
admin.site.register(Group)
