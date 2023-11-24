
from django.contrib.auth.decorators import permission_required
from django.shortcuts import redirect

from django.contrib.auth.mixins import UserPassesTestMixin
from django.utils.decorators import method_decorator
from django.views import View
from django.contrib import messages
from .models import Employee
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.http import JsonResponse
from .forms import EmployeeForm
from .forms import Step3Form  # Replace with the actual import path
from .models import Step1Sub1, Step1Sub2, Step1Sub3, Step1Sub4, Step2, Step3
from .forms import Step3Form
from .models import Step2, Step3
from .models import Step2
from .forms import Step2Form
from .models import Step1Sub1, Step1Sub4
from django.shortcuts import render
from django.db import connections
from django.core.management.base import BaseCommand
from .models import Step1Sub4
from .forms import Step1Sub4Form
from .models import UserProfile
from .models import Step1Sub1, Step1Sub2, Step1Sub3
from .forms import Step1Sub3Form
from .models import Step1Sub2
from .forms import Step1Sub2Form
from django.shortcuts import render, redirect
from .models import Step1Sub1
from .forms import Step1Sub1Form
import uuid
from django.shortcuts import render, HttpResponseRedirect, HttpResponse, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from payroll import settings
from django.core.mail import send_mail
from django.contrib.auth.views import PasswordResetView
from .forms import *
from .models import *

from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from .helpers import send_reset_password_email
from django.contrib.auth.decorators import login_required
from .forms import Step1Sub3Form
# Create your views here.


def home(request):
    return render(request, "payrollapp/home.html")


def about(request):
    return render(request, "payrollapp/about.html")


def contact(request):
    return render(request, "payrollapp/contact.html")

    # return render(request, 'payrollapp/signup.html')


def user_signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            selected_group_name = form.cleaned_data['your_title']
            selected_group, created = Group.objects.get_or_create(
                name=selected_group_name)
            selected_group.user_set.add(user)

            # Create the user profile with first_login set to True
            user_profile = UserProfile(
                user=user, first_login=True, first_name=form.cleaned_data['first_name'])
            user_profile.save()

            un = form.cleaned_data['username']
            fn = form.cleaned_data['first_name']
            ln = form.cleaned_data['last_name']
            em = form.cleaned_data['email']
            pw1 = form.cleaned_data['password1']
            pw2 = form.cleaned_data['password2']

            current_site = get_current_site(request)
            mail_subject = 'Activation link has been sent to your Email ID'
            message = render_to_string('payrollapp/acc_activate_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })

            to_email = em
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()

            if User.objects.filter(username=un).exists():
                messages.error(
                    request, "Username already exists, please try another username.")
                return HttpResponseRedirect('/signup/')

            if User.objects.filter(email=em).exists():
                messages.error(
                    request, "Email already exists, Please try another Email ID! ")
                return HttpResponseRedirect('/')

            if len(un) > 10:
                messages.error(request, "Username must be under 10 characters")

            if not un.isalnum():
                messages.error(request, "Username must be Alpha Numeric")
                return HttpResponseRedirect('/')

            messages.success(
                request, "Please confirm your email address to complete registration")
            return HttpResponseRedirect('/')

        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
            return render(request, 'payrollapp/signup.html', {'form': form})

    form = SignUpForm()
    return render(request, 'payrollapp/signup.html', {'form': form})


def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return render(request, 'payrollapp/signup_activate.html')
    else:
        return HttpResponse("Activation Invalid")
 

def log_in(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            form = LoginForm(request=request, data=request.POST)
            if form.is_valid():
                uname = form.cleaned_data['username']
                upass = form.cleaned_data['password']
                user = authenticate(username=uname, password=upass)
                if user is not None:
                    login(request, user)

                    # Check if it's the user's first login
                    try:
                        user_profile = UserProfile.objects.get(user=user)
                        if user_profile.first_login:
                            user_profile.first_login = False
                            # user_profile.first_name = user.first_name
                            user_profile.save()
                            return HttpResponseRedirect('/step-1-sub-1/')
                        else:
                            # return HttpResponseRedirect('/dashboard/')
                            first_name = user.first_name
                            print("First Name:", first_name)  # Add this line
                            return render(request, 'payrollapp/dashboard_base.html', {'user_first_name': first_name})

                    except UserProfile.DoesNotExist:
                        pass  # Handle the case when UserProfile does not exist

        else:
            form = LoginForm()
        return render(request, 'payrollapp/login.html', {'form': form})
    else:
        return HttpResponseRedirect('/dashboard/')


def dashboard(request):
    context = {'dashboard': 'active'}
    if request.user.is_authenticated:
        user_profile = UserProfile.objects.get(user=request.user)
        if user_profile.first_login:
            # Redirect to setup.html
            return redirect('/step-1-sub-1/')
        else:

            return render(request, 'payrollapp/dashboard.html', context)
    else:
        return HttpResponseRedirect('/login/')


def setup(request):
    if request.user.is_authenticated:
        user_profile = UserProfile.objects.get(user=request.user)

        # Check if it's the user's first login
        if user_profile.first_login:
            # If it's the first login, set first_login to False and render the setup.html template
            user_profile.first_login = False
            user_profile.save()
            return render(request, 'payrollapp/step_1_sub_1.html')
        else:
            # If it's not the first login, redirect to the dashboard
            return redirect('dashboard')
    else:
        return redirect('login')


def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')


def password_reset_confirm(request, token):
    context = {}

    try:
        profile_obj = Profile.objects.filter(
            reset_password_token=token).first()
        context = {'user_id': profile_obj.user.id}

        if request.method == 'POST':
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('reconfirm_password')
            user_id = request.POST.get('user_id')

            if user_id is None:
                messages.success(request, 'No user id found.')
                return redirect(f'/password_reset_confirm/{token}/')

            if new_password != confirm_password:
                messages.success(request, 'Both passwords should be equal.')
                return redirect(f'/password_reset_confirm/{token}/')

            user_obj = User.objects.get(id=user_id)
            user_obj.set_password(new_password)
            user_obj.save()
            return redirect('/login/')

    except Exception as e:
        print(e)

    return render(request, 'payrollapp/change_password.html', context)


def password_reset_done(request):
    return render(request, 'payrollapp/password_reset_done.html')


def password_reset_request(request):
    if request.method == 'POST':
        form = PasswordResetEmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = User.objects.filter(email=email).first()

            if user:
                # Generate a reset password token and send an email
                token = str(uuid.uuid4())
                profile, created = Profile.objects.get_or_create(user=user)
                profile.reset_password_token = token
                profile.save()

                # Send an email to the user with a link to reset the password
                send_reset_password_email(email, token)

                messages.success(
                    request, 'An email has been sent with instructions to reset your password.')
            else:
                messages.error(request, 'No user found with this email.')

            return redirect('/password_reset_done/')

    form = PasswordResetEmailForm()
    return render(request, 'payrollapp/forget-password.html', {'form': form})


@login_required
def step_1_sub_1(request):
    user = request.user

    if request.method == 'POST':
        form = Step1Sub1Form(request.POST)

        # Set the required field as not required for "Don't have GST" button
        if 'no_gst' in request.POST:
            form.fields['company_gstin'].required = False

        if form.is_valid():
            # Reset the required attribute to its original state
            form.fields['company_gstin'].required = True

            if 'no_gst' in request.POST:
                # Redirect to step-1-sub-2 without processing the form
                return redirect('step_1_sub_2')
            elif 'continue' in request.POST:
                # Continue with form processing
                data, created = Step1Sub1.objects.get_or_create(user=user)
                data.company_gstin = form.cleaned_data['company_gstin']
                data.save()

                return redirect('step_1_sub_4')
    else:
        try:
            data = Step1Sub1.objects.get(user=user)
            form = Step1Sub1Form(instance=data)
        except Step1Sub1.DoesNotExist:
            form = Step1Sub1Form()

    return render(request, 'payrollapp/step_1_sub_1.html', {'form': form})

# views.py


@login_required
def step_1_sub_2(request):
    user = request.user

    if request.method == 'POST':
        form = Step1Sub2Form(request.POST)
        if form.is_valid():
            data, created = Step1Sub2.objects.get_or_create(user=user)
            data.organization_type = form.cleaned_data['organization_type']
            data.company_pan = form.cleaned_data['company_pan']
            data.save()
            return redirect('step_1_sub_3')
    else:
        try:
            data = Step1Sub2.objects.get(user=user)
            form = Step1Sub2Form(instance=data)
        except Step1Sub2.DoesNotExist:
            form = Step1Sub2Form()

    return render(request, 'payrollapp/step_1_sub_2.html', {'form': form})


# views.py
@login_required
def step_1_sub_3(request):
    user = request.user
    try:
        step1_sub2_data = Step1Sub2.objects.get(user=user)
    except Step1Sub2.DoesNotExist:
        return redirect('step_1_sub_2')

    existing_instance = Step1Sub3.objects.filter(
        step1_sub2_data=step1_sub2_data).first()

    if request.method == 'POST':
        form = Step1Sub3Form(
            request.POST, step1_sub2_data_instance=step1_sub2_data, instance=existing_instance)
        if form.is_valid():
            form.instance.step1_sub2_data = step1_sub2_data
            form.save()
            return redirect('#')  # Redirect to the next step
    else:
        form = Step1Sub3Form(
            step1_sub2_data_instance=step1_sub2_data, instance=existing_instance)

    return render(request, 'payrollapp/step_1_sub_3.html', {'form': form})


# **********************************************************
# Sub1Sub4 View


@login_required
def step_1_sub_4(request):
    user = request.user

    try:
        step1_sub1_data = Step1Sub1.objects.get(user=user)
        company_gstin_from_sub1 = step1_sub1_data.company_gstin
    except Step1Sub1.DoesNotExist:
        company_gstin_from_sub1 = None

    form = None

    if request.method == 'POST':
        form = Step1Sub4Form(
            request.POST, company_gstin_from_sub1=company_gstin_from_sub1)
        if form.is_valid():
            data, created = Step1Sub4.objects.get_or_create(user=user)
            data.brand_name = form.cleaned_data['brand_name']
            data.organization_type = form.cleaned_data['organization_type']
            data.company_gstin = company_gstin_from_sub1
            data.company_pan = form.cleaned_data['company_pan']
            data.company_name = form.cleaned_data['company_name']
            data.registered_address = form.cleaned_data['registered_address']
            data.pincode = form.cleaned_data['pincode']
            data.state = form.cleaned_data['state']
            data.save()

            # return render(request, 'payrollapp/confirmation_popup.html')

    else:
        try:
            data = Step1Sub4.objects.get(user=user)
            form = Step1Sub4Form(
                instance=data, company_gstin_from_sub1=company_gstin_from_sub1)
        except Step1Sub4.DoesNotExist:
            form = Step1Sub4Form(
                company_gstin_from_sub1=company_gstin_from_sub1)

    return render(request, 'payrollapp/step_1_sub_4.html', {'form': form})


@login_required
def success_view(request):
    return render(request, 'payrollapp/success.html')


# ****************************************************************


@login_required
def step_2(request):
    user = request.user
    try:
        step2_instance = Step2.objects.get(user=user)
    except Step2.DoesNotExist:
        step2_instance = None

    if request.method == 'POST':
        form = Step2Form(request.POST, instance=step2_instance)
        if form.is_valid():
            form.instance.user = user
            form.save()
            # Update the visibility context variable based on the checkbox value
            is_payroll_enabled = form.cleaned_data.get(
                'payroll_enabled', False)
            return render(request, 'payrollapp/step_2.html', {'form': form, 'is_payroll_enabled': is_payroll_enabled})
    else:
        form = Step2Form(instance=step2_instance)

    return render(request, 'payrollapp/step_2.html', {'form': form})

# ******************************************************


@login_required
def step_3(request):
    user = request.user

    # Check if the user has completed previous steps
    if not Step1Sub1.objects.filter(user=user).exists() or not Step2.objects.filter(user=user).exists():
        messages.error(
            request, 'Please complete the previous steps before proceeding.')
        return render(request, 'payrollapp/step_3.html', {'form': None})

    try:
        step3_instance = Step3.objects.get(user=user)
    except Step3.DoesNotExist:
        step3_instance = None

    if request.method == 'POST':
        form = Step3Form(request.POST, instance=step3_instance)
        if form.is_valid():
            form.instance.user = user
            form.save()

            # Add a success message to the session
            messages.success(request, 'Step 3 completed successfully.')

            # Redirect to the dashboard after completing Step 3
            return redirect('dashboard')  # Adjust the URL name as needed
    else:
        form = Step3Form(instance=step3_instance)

    return render(request, 'payrollapp/step_3.html', {'form': form})


# People


@login_required
def people(request):
    if request.user.groups.filter(name='Employees').exists() and request.path_info == reverse('people'):
        return redirect('restrict')
    all_employees = Employee.objects.values(
        'name', 'job_title', 'employee_type')
    employees = all_employees.filter(employee_type='Employee')
    contractors = all_employees.filter(employee_type='Contractor')
    search_query = request.GET.get('search', '')

    if search_query:
        all_employees = all_employees.filter(
            name__icontains=search_query) | all_employees.filter(job_title__icontains=search_query)
        employees = employees.filter(name__icontains=search_query) | employees.filter(
            job_title__icontains=search_query)
        contractors = contractors.filter(name__icontains=search_query) | contractors.filter(
            job_title__icontains=search_query)

    context = {
        'all_employees': all_employees,
        'employees': employees,
        'contractors': contractors,
        'active_tab': request.GET.get('tab', 'all'),
        'people': 'active',
        'search_query': search_query,
    }

    return render(request, 'payrollapp/dashboard_people.html', context)


# def peopleaddone(request):
#     if request.user.is_authenticated:
#         return render(request, 'payrollapp/dashboard_people_addone.html')
#     else:
#         return HttpResponseRedirect('/login/')


# ************************************************************************
# Add one


@login_required
def addone_employee(request):
    if request.user.groups.filter(name='Employees').exists() and request.path_info == reverse('addone_employee'):
        return redirect('restrict')

    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True, 'message': 'Your account has been added.', 'redirect_url': reverse('people')})
        else:
            errors = {field: [error for error in errors]
                      for field, errors in form.errors.items()}
            return JsonResponse({'success': False, 'errors': errors})
    else:
        form = EmployeeForm()

    return render(request, 'payrollapp/dashboard_people_addone.html', {'form': form})


# Payslips


@login_required
def MyPaySlips(request):
    context = {'mypayslips': 'active'}
    if request.user.is_authenticated:
        return render(request, 'payrollapp/mypayslips.html', context)
    else:
        return HttpResponseRedirect('/login/')

# Attendance


@login_required
def Attendance(request):
    context = {'attendance': 'active'}
    if request.user.is_authenticated:
        return render(request, 'payrollapp/attendance.html', context)
    else:
        return HttpResponseRedirect('/login/')

# taxdeduction


@login_required
def TaxDeduction(request):
    context = {'taxdeduction': 'active'}
    if request.user.is_authenticated:
        return render(request, 'payrollapp/taxdeduction.html', context)
    else:
        return HttpResponseRedirect('/login/')

# reimbursements


@login_required
def Reimbursements(request):
    context = {'reimbursements': 'active'}
    if request.user.is_authenticated:
        return render(request, 'payrollapp/reimbursements.html', context)
    else:
        return HttpResponseRedirect('/login/')


# Documents
@login_required
def Documents(request):
    context = {'documents': 'active'}
    if request.user.is_authenticated:
        return render(request, 'payrollapp/documents.html', context)
    else:
        return HttpResponseRedirect('/login/')

# Help


@login_required
def Help(request):
    context = {'help': 'active'}
    if request.user.is_authenticated:
        return render(request, 'payrollapp/help.html', context)
    else:
        return HttpResponseRedirect('/login/')


def restrict_view(request):
    return render(request, 'payrollapp/dashboard_restricted.html')
