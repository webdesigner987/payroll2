from django.core.validators import RegexValidator
from django.contrib.auth.models import User, Group
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    reset_password_token = models.CharField(
        max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    first_login = models.BooleanField(
        default=True)  # Add the first_login field

    def __str__(self):
        return self.user.username


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30, default='default_first_name')
    first_login = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username


class Step1Sub1(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company_gstin = models.CharField(max_length=15)

    def __str__(self):
        return self.company_gstin


class Step1Sub2(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    organization_type = models.CharField(max_length=255)
    company_pan = models.CharField(max_length=255)

    def get_organization_type(self):
        return self.organization_type

    def __str__(self):
        return f"{self.organization_type} - {self.company_pan}"


# models.py
def validate_pincode(value):
    # Check if the pincode is exactly six digits
    if len(value) != 6:
        raise ValidationError(_('Pincode must be six digits'))

    # Check if the first digit is between 1 and 9
    if not ('1' <= value[0] <= '9'):
        raise ValidationError(
            _('First digit of the pincode must be between 1 and 9'))

    # Check if the next five digits are numeric
    if not value[1:].isdigit():
        raise ValidationError(
            _('The next five digits of the pincode must be numeric'))

    # Check for the optional space after three digits
    if len(value) == 7 and value[3] != ' ':
        raise ValidationError(_('Invalid format for pincode'))


STATE_CHOICES = [
    ('Andhra Pradesh', 'Andhra Pradesh'),
    ('Arunachal Pradesh', 'Arunachal Pradesh'),
    ('Assam', 'Assam'),
    ('Bihar', 'Bihar'),
    ('Chhattisgarh', 'Chhattisgarh'),
    # Add other states as needed
]


class Step1Sub3(models.Model):
    brand_name = models.CharField(max_length=255)
    step1_sub2_data = models.OneToOneField(
        Step1Sub2, on_delete=models.CASCADE, related_name='step1_sub3_data')
    work_address = models.TextField(blank=True, null=True)
    pincode = models.CharField(max_length=10, validators=[
                               validate_pincode], default='')
    state = models.CharField(
        max_length=255, choices=STATE_CHOICES, default='Andhra Pradesh')

    def get_organization_type(self):
        return self.step1_sub2_data.organization_type

    def get_company_pan(self):
        return self.step1_sub2_data.company_pan


# **********************************************************************************
# sub1Sub4 form


def validate_company_pan(value):
    if len(value) != 10:
        raise ValidationError(_("Company PAN must be ten characters long."))

    if not value[:5].isalpha():
        raise ValidationError(
            _("First five characters of Company PAN must be any uppercase alphabets."))

    if not value[5:9].isdigit():
        raise ValidationError(
            _("Next four characters of Company PAN must be any number from 0 to 9."))

    if not value[9].isalpha():
        raise ValidationError(
            _("Last (tenth) character of Company PAN must be any uppercase alphabet."))

    if ' ' in value:
        raise ValidationError(
            _("Company PAN should not contain any white spaces."))


def validate_pincode(value):
    if len(value) != 6:
        raise ValidationError(_("Pincode must be six digits."))

    if value.startswith('0'):
        raise ValidationError(_("Pincode should not start with zero."))

    if not value[0].isdigit() or not value[1:].isdigit():
        raise ValidationError(_("Invalid Pincode format."))


class Step1Sub4(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    brand_name = models.CharField(max_length=255, verbose_name='Brand Name')
    organization_type = models.CharField(
        max_length=10,
        choices=[('private', 'Private'), ('govt', 'Government')],
        verbose_name='Organization Type*',
    )
    company_gstin = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        verbose_name='Company GSTIN',
        help_text='If you want to change, go back and change GST Number.',
    )
    company_pan = models.CharField(
        max_length=10,
        verbose_name='Company PAN',
        help_text='It should be ten characters long. The first five characters should be any upper case alphabets. '
                  'The next four characters should be any number from 0 to 9. '
                  'The last (tenth) character should be any upper case alphabet. '
                  'It should not contain any white spaces.',
    )
    company_name = models.CharField(
        max_length=255, verbose_name='Company Name')
    registered_address = models.TextField(verbose_name='Registered Address')
    pincode = models.CharField(
        max_length=10,
        verbose_name='Pincode',
        help_text='It can be only six digits. It should not start with zero. '
                  'First digit of the pin code must be from 1 to 9. '
                  'Next five digits of the pin code may range from 0 to 9. '
                  'It should allow only one white space, but after three digits, although this is optional.',
    )
    state = models.CharField(
        max_length=20,
        choices=[('state-a', 'State A'), ('state-b',
                                          'State B'), ('state-c', 'State C')],
        verbose_name='State',
    )

    def __str__(self):
        return f"{self.user.username}'s Step1Sub4 Data"


# models.py

class Step2(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    payroll_enabled = models.BooleanField(default=False)
    payroll_date = models.IntegerField(choices=[(
        1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7')], blank=True, null=True)
    auto_run_payroll = models.BooleanField(default=False)
    employee_request_advance = models.BooleanField(default=False)

# *****************************


class Step3(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    use_default_salary_structure = models.BooleanField(default=False)
    if_good_description = models.TextField(blank=True)
    consider_fbp = models.BooleanField(default=False)


# ***********************************************************************************
# Add one


class Employee(models.Model):
    employee_type = models.CharField(
        max_length=20,
        choices=[
            ('Employee', 'Employee'),
            ('Contractor', 'Contractor')],
        default=''
    )
    name = models.CharField(max_length=100, default='')
    email = models.EmailField(default='')
    hire_date = models.DateField()
    job_title = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    manager = models.CharField(
        max_length=10,
        choices=[
            ('emp01', 'emp01'),
            ('emp02', 'emp02')]
    )
    annual_salary = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.CharField(
        max_length=20,
        choices=[
            ('State01', 'State01'),
            ('State02', 'State02')]
    )
    resident_of_india = models.BooleanField(default=False)
    pan_number = models.CharField(max_length=20, default='')
    ifsc_code = models.CharField(max_length=11, default='')
    account_number = models.CharField(max_length=18, default='')
    beneficiary_name = models.CharField(max_length=100, default='')

    pf_status = models.CharField(
        max_length=10,
        choices=[
            ('Opt In', 'Opt In'),
            ('Opt Out', 'Opt Out')],
        default=''
    )

    provident_fund_uan = models.CharField(
        max_length=12,
        validators=[RegexValidator(
            regex=r'^\d{12}$', message="Provident Fund UAN must be a 12-digit number.")],
        default=''
    )

    pf_wages_calculation = models.CharField(
        max_length=20,
        choices=[
            ('Company Default', 'Company Default'),
            ('Under 15000', 'Under 15000'),
            ('No Limit', 'No Limit')],
        default=''
    )

    include_employer_contribution = models.CharField(
        max_length=20,
        choices=[
            ('Company Default', 'Company Default'),
            ('Yes', 'Yes'),
            ('No', 'No')],
        default=''
    )

    contribute_to_pf_eps = models.BooleanField(default=False)

    pt_status = models.CharField(
        max_length=10,
        choices=[
            ('Enabled', 'Enabled'),
            ('Disabled', 'Disabled')],
        default=''
    )

    pt_location = models.CharField(
        max_length=20,
        choices=[
            ('State 01', 'State 01'),
            ('State 02', 'State 02')],
        default=''
    )

    def clean(self):
        errors = []

        if not (len(self.ifsc_code) == 11 and self.ifsc_code[:4].isalpha() and self.ifsc_code[4] == '0' and self.ifsc_code[5:].isdigit()):
            errors.append(ValidationError(
                {'ifsc_code': "Invalid IFSC Code. Please follow the specified format and use capital letters."}))

        account_number = self.account_number.strip()
        if not (account_number.isdigit() and 9 <= len(account_number) <= 18):
            errors.append(ValidationError(
                {'account_number': "Invalid Account Number. It should be a numeric value with a length between 9 and 18 digits, and no whitespaces or special characters are allowed."}))

        if not (len(self.pan_number) == 10 and self.pan_number[:5].isalpha() and self.pan_number[5:9].isdigit() and self.pan_number[9].isalpha() and not self.pan_number.isspace()):
            errors.append(ValidationError(
                {'pan_number': "Invalid PAN Number. Please follow the specified format."}))

        provident_fund_uan = self.provident_fund_uan.strip()
        if not (provident_fund_uan.isdigit() and len(provident_fund_uan) == 12):
            errors.append(ValidationError(
                {'provident_fund_uan': "Provident Fund UAN must be a 12-digit number."}))

        if errors:
            raise ValidationError(errors)

        return super().clean()


# Groups


def create_groups():
    # Create or get the Founder group
    founder_group, created = Group.objects.get_or_create(name='Founder')
    if created:
        print('Founder group created.')

    # Create or get the HR Admin group
    hr_admin_group, created = Group.objects.get_or_create(name='HR Admin')
    if created:
        print('HR Admin group created.')

    # Create or get the Employees group
    employees_group, created = Group.objects.get_or_create(name='Employees')
    if created:
        print('Employees group created.')


# Call the function to create groups when the app is ready
create_groups()
