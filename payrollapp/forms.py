from django.core.exceptions import ValidationError
from .models import Employee
from .models import Step3  # Import your Step3 model
from .models import Step2
from .models import Step1Sub4
from .models import Step1Sub3
from .models import Step1Sub2
from .models import Step1Sub1
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField
from django.contrib.auth.models import User
from django.utils.translation import gettext, gettext_lazy as _
from django.core.validators import RegexValidator
from .models import *
import re
from django.contrib.auth.models import Group


class SignUpForm(UserCreationForm):

    organization_name = forms.CharField(
        label='Organization Name', required=True, widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    phone_regex = RegexValidator(
        regex=r'^\d{10}$',
        message="Phone number must be exactly 10 digits without spaces or special characters.",
    )

    phone_number = forms.CharField(
        label='Phone Number',
        required=True,
        validators=[phone_regex],
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    NUMBER_OF_EMPLOYEES_CHOICES = [
        ('1-10', '1-10 Employees'),
        ('11-50', '11-50 Employees'),
        ('51-100', '51-100 Employees'),
        ('101-500', '101-500 Employees'),
        ('501+', '501+ Employees'),
    ]

    number_of_employees = forms.ChoiceField(
        label='Number of Employees',
        required=True,
        choices=NUMBER_OF_EMPLOYEES_CHOICES,
        widget=forms.Select(
            attrs={'class': 'form-control', 'style': 'background-color: #393f5c;color :white; border:0; border-radius:0'}),
    )

    group_choices = [(group.name, group.name.capitalize())
                     for group in Group.objects.all()]

    your_title = forms.ChoiceField(
        label='Your Title',
        required=True,
        choices=group_choices,
        widget=forms.Select(attrs={
                            'class': 'form-control', 'style': 'background-color: #393f5c;color :white; border:0; border-radius:0'}),
    )

    password1 = forms.CharField(
        label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(
        label='Confirm Password (again)', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'first_name',
                  'last_name', 'organization_name', 'email', 'phone_number', 'number_of_employees', 'your_title']
        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'email': 'Enter your Email ID',
            'organization_name': 'Organization Name',
            'phone_number': 'Phone Number',
            'number_of_employees': 'Number of Employees',
            'your_title': 'Your Title',
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'organization_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'number_of_employees': forms.Select(attrs={'class': 'form-control'}),
            'your_title': forms.Select(attrs={'class': 'form-control'}),

        }


class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(
        attrs={'autofocus': True, 'class': 'form-control'}))
    password = forms.CharField(label=_('Password'), strip=False, widget=forms.PasswordInput(
        attrs={'autocomplete': 'current-password', 'class': 'form-control'}))


class PasswordResetEmailForm(forms.Form):
    email = forms.EmailField(max_length=254, widget=forms.EmailInput(
        attrs={'class': 'form-control'}))


# forms.py


class Step1Sub1Form(forms.ModelForm):
    class Meta:
        model = Step1Sub1
        fields = ['company_gstin']
        labels = {
            'company_gstin': 'Company GSTIN*',
        }
        widgets = {
            'company_gstin': forms.TextInput(attrs={'class': 'form-control', 'autofocus': True}),
        }


# forms.py

ORGANIZATION_CHOICES = [
    ('private', 'Private'),
    ('govt', 'Government'),
]


class Step1Sub2Form(forms.ModelForm):
    organization_type = forms.ChoiceField(
        label='Organization Type*',
        widget=forms.Select(attrs={
                            'class': 'form-control', 'style': 'background-color: #393f5c;color :white; border:0; border-radius:0'}),
        choices=ORGANIZATION_CHOICES,
        help_text='Select the organization type',
    )

    class Meta:
        model = Step1Sub2
        fields = ['organization_type', 'company_pan']
        labels = {
            'company_pan': 'Company PAN*',
        }
        widgets = {
            'company_pan': forms.TextInput(attrs={'class': 'form-control', 'autofocus': True}),
        }

    def clean_company_pan(self):
        company_pan = self.cleaned_data['company_pan']

        # Define a regular expression pattern for the desired format
        pattern = re.compile(r'^[A-Z]{3}[T|F|H|P|C][A-Z][0-9]{4}[A-Z]$')

        if not pattern.match(company_pan):
            raise forms.ValidationError(
                "Invalid Company PAN format. It must be in the format ABCXT0000X.")

        return company_pan


class Step1Sub3Form(forms.ModelForm):
    organization_type = forms.CharField(
        label='Organization Type',
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'readonly': 'readonly'}),
    )
    company_pan = forms.CharField(
        label='Company PAN',
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'readonly': 'readonly'}),
    )

    work_address = forms.CharField(
        label='Work Address*',
        widget=forms.Textarea(
            attrs={'class': 'form-control', 'rows': 3, 'required': 'required', 'style': 'background-color: #393f5c;color :white; border:0; border-radius:0'}),
    )
    pincode = forms.CharField(
        label='Pincode*',
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'required': 'required'}),
        help_text='Enter your pincode'
    )
    state = forms.ChoiceField(
        label='State*',
        widget=forms.Select(attrs={
                            'class': 'form-control', 'style': 'background-color: #393f5c;color :white; border:0; border-radius:0'}),
        choices=STATE_CHOICES,
    )

    class Meta:
        model = Step1Sub3
        fields = ['brand_name', 'organization_type',
                  'company_pan', 'work_address', 'pincode', 'state']
        labels = {
            'brand_name': 'Brand Name*',
        }
        widgets = {
            'brand_name': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        step1_sub2_data_instance = kwargs.pop('step1_sub2_data_instance', None)
        super(Step1Sub3Form, self).__init__(*args, **kwargs)

        if step1_sub2_data_instance:
            # Set to empty, allowing user input
            self.fields['brand_name'].initial = ''
            self.fields['organization_type'].initial = step1_sub2_data_instance.organization_type
            self.fields['company_pan'].initial = step1_sub2_data_instance.company_pan


# ?**************************************************
# Sub1Sub4 Form


class Step1Sub4Form(forms.ModelForm):
    brand_name = forms.CharField(
        label='Brand Name*',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        help_text='Kindly enter your Brand Name',
        required=True,
    )

    organization_type = forms.ChoiceField(
        label='Organization Type*',
        widget=forms.Select(attrs={
                            'class': 'form-control', 'style': 'background-color: #393f5c;color :white; border:0; border-radius:0'}),
        choices=[('private', 'Private'), ('govt', 'Government')],
        help_text='Select the organization type',
        required=True,
    )

    company_gstin = forms.CharField(
        label='Company GSTIN*',
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'readonly': True}),
        help_text='This field is read-only. If you want to change it, please go back to Step 1.',
        required=True,
    )

    company_pan = forms.CharField(
        label='Company PAN*',
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'autofocus': True}),
        help_text='It should be ten characters long. The first five characters should be any upper case alphabets. The next four characters should be any number from 0 to 9. The last (tenth) character should be any upper case alphabet. It should not contain any white spaces.',
        max_length=10,
        required=True,
    )

    company_name = forms.CharField(
        label='Company Name*',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=True,
    )

    registered_address = forms.CharField(
        label='Registered Address*',
        widget=forms.Textarea(
            attrs={'class': 'form-control', 'rows': 2, 'required': 'required', 'style': 'background-color: #393f5c;color :white; border:0; border-radius:0'}),
        required=True,
    )

    pincode = forms.CharField(
        label='Pincode*',
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'required': 'required'}),
        help_text='It can be only six digits. It should not start with zero. First digit of the pin code must be from 1 to 9. Next five digits of the pin code may range from 0 to 9. It should allow only one white space, but after three digits, although this is optional.',
        required=True,
    )

    state_choices = [
        ('state-a', 'State A'),
        ('state-b', 'State B'),
        ('state-c', 'State C'),
    ]
    state = forms.ChoiceField(
        label='State*',
        widget=forms.Select(attrs={
                            'class': 'form-control', 'style': 'background-color: #393f5c;color :white; border:0; border-radius:0'}),
        choices=state_choices,
        required=True,
    )

    class Meta:
        model = Step1Sub4
        fields = ['brand_name', 'organization_type', 'company_gstin', 'company_pan',
                  'company_name', 'registered_address', 'pincode', 'state']

    def __init__(self, *args, **kwargs):
        company_gstin_from_sub1 = kwargs.pop('company_gstin_from_sub1', None)
        super(Step1Sub4Form, self).__init__(*args, **kwargs)

        if company_gstin_from_sub1 is not None:
            self.fields['company_gstin'].initial = company_gstin_from_sub1
# **************************************************************************


class Step2Form(forms.ModelForm):
    class Meta:
        model = Step2
        fields = ['payroll_enabled', 'payroll_date',
                  'auto_run_payroll', 'employee_request_advance']
        widgets = {
            'payroll_enabled': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'payroll_date': forms.Select(attrs={'class': 'form-control', 'style': 'background-color: #393f5c;color :white; border:0; border-radius:0'}),
            'auto_run_payroll': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'employee_request_advance': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        help_texts = {
            'payroll_enabled': 'Description for Payroll Enabled',
            'payroll_date': 'Description for Payroll Date',
            'auto_run_payroll': 'Description for Automatic Run Payroll',
            'employee_request_advance': 'Description for Employee Request Salary Advance',
        }


# ********************************************
# payrollapp/forms.py


class Step3Form(forms.ModelForm):
    class Meta:
        model = Step3
        fields = ['use_default_salary_structure', 'consider_fbp']

    use_default_salary_structure = forms.BooleanField(
        label="Use xpayroll's default salary structure",
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    consider_fbp = forms.BooleanField(
        label="Consider FBP",
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    def __init__(self, *args, **kwargs):
        super(Step3Form, self).__init__(*args, **kwargs)


# ************************************************************************
# Add one
# forms.py


class EmployeeForm(forms.ModelForm):
    # ... other form fields and methods ...

    def clean_ifsc_code(self):
        ifsc_code = self.cleaned_data.get('ifsc_code', '').strip().upper()

        # Check if the field is required and if the value is not empty
        if self.fields['ifsc_code'].required and not ifsc_code:
            raise forms.ValidationError("This field is required.")

        # Custom validation for IFSC code format
        if ifsc_code and not (len(ifsc_code) == 11 and ifsc_code[:4].isalpha() and ifsc_code[4] == '0' and ifsc_code[5:].isdigit()):
            raise forms.ValidationError(
                "Invalid IFSC Code. Please follow the specified format and use capital letters.")

        return ifsc_code

    def clean_account_number(self):
        account_number = self.cleaned_data['account_number'].strip()
        if not (account_number.isdigit() and 9 <= len(account_number) <= 18):
            raise forms.ValidationError(
                "Invalid Account Number. It should be a numeric value with a length between 9 and 18 digits, and no whitespaces or special characters are allowed.")
        return account_number

    def clean_provident_fund_uan(self):
        provident_fund_uan = self.cleaned_data['provident_fund_uan']
        if not provident_fund_uan.isdigit() or len(provident_fund_uan) != 12:
            raise forms.ValidationError(
                "Provident Fund UAN must be a 12-digit number.")
        return provident_fund_uan

    class Meta:
        model = Employee
        fields = '__all__'
        widgets = {
            'employee_type': forms.Select(attrs={'class': 'form-select', 'style': 'background-color: #393f5c;color :white; border:0; border-radius:0'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'style': 'background-color: #393f5c;color :white; border:0; border-radius:0', 'style': 'background-color: #393f5c;color :white; border:0; border-radius:0', 'style': 'background-color: #393f5c;color :white; border:0; border-radius:0'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'style': 'background-color: #393f5c;color :white; border:0; border-radius:0', 'style': 'background-color: #393f5c;color :white; border:0; border-radius:0'}),
            'hire_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'style': 'background-color: #393f5c;color :white; border:0; border-radius:0', 'style': 'background-color: #393f5c;color :white; border:0; border-radius:0'}),
            'job_title': forms.TextInput(attrs={'class': 'form-control', 'style': 'background-color: #393f5c;color :white; border:0; border-radius:0', 'style': 'background-color: #393f5c;color :white; border:0; border-radius:0'}),
            'department': forms.TextInput(attrs={'class': 'form-control', 'style': 'background-color: #393f5c;color :white; border:0; border-radius:0', 'style': 'background-color: #393f5c;color :white; border:0; border-radius:0'}),
            'manager': forms.Select(attrs={'class': 'form-select', 'style': 'background-color: #393f5c;color :white; border:0; border-radius:0', 'style': 'background-color: #393f5c;color :white; border:0; border-radius:0'}),
            'annual_salary': forms.NumberInput(attrs={'class': 'form-control', 'style': 'background-color: #393f5c;color :white; border:0; border-radius:0', 'style': 'background-color: #393f5c;color :white; border:0; border-radius:0'}),
            'location': forms.Select(attrs={'class': 'form-select', 'style': 'background-color: #393f5c;color :white; border:0; border-radius:0', 'style': 'background-color: #393f5c;color :white; border:0; border-radius:0'}),
            'resident_of_india': forms.CheckboxInput(attrs={'class': 'form-check-input', 'style': 'background-color: #393f5c;color :white; border:0; border-radius:0', 'style': 'background-color: #393f5c;color :white; border:0; border-radius:0'}),
            'pan_number': forms.TextInput(attrs={'class': 'form-control', 'style': 'background-color: #393f5c;color :white; border:0; border-radius:0', 'style': 'background-color: #393f5c;color :white; border:0; border-radius:0'}),
            'ifsc_code': forms.TextInput(attrs={'class': 'form-control', 'style': 'background-color: #393f5c;color :white; border:0; border-radius:0', 'style': 'background-color: #393f5c;color :white; border:0; border-radius:0'}),
            'account_number': forms.TextInput(attrs={'class': 'form-control', 'style': 'background-color: #393f5c;color :white; border:0; border-radius:0'}),
            'beneficiary_name': forms.TextInput(attrs={'class': 'form-control', 'style': 'background-color: #393f5c;color :white; border:0; border-radius:0'}),
            'pf_status': forms.Select(attrs={'class': 'form-select', 'style': 'background-color: #393f5c;color :white; border:0; border-radius:0'}),
            'provident_fund_uan': forms.TextInput(attrs={'class': 'form-control', 'style': 'background-color: #393f5c;color :white; border:0; border-radius:0'}),
            'pf_wages_calculation': forms.Select(attrs={'class': 'form-select', 'style': 'background-color: #393f5c;color :white; border:0; border-radius:0'}),
            'include_employer_contribution': forms.Select(attrs={'class': 'form-select', 'style': 'background-color: #393f5c;color :white; border:0; border-radius:0'}),
            'contribute_to_pf_eps': forms.CheckboxInput(attrs={'class': 'form-check-input', 'style': 'background-color: #393f5c;color :white; border:0; border-radius:0'}),
            'pt_status': forms.Select(attrs={'class': 'form-select', 'style': 'background-color: #393f5c;color :white; border:0; border-radius:0'}),
            'pt_location': forms.Select(attrs={'class': 'form-select', 'style': 'background-color: #393f5c;color :white; border:0; border-radius:0'}),
        }
