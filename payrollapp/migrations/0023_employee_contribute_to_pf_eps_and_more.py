# Generated by Django 4.2.7 on 2023-11-23 19:04

import django.core.validators
from django.db import migrations, models
import payrollapp.models


class Migration(migrations.Migration):

    dependencies = [
        ('payrollapp', '0022_alter_step1sub3_pincode'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='contribute_to_pf_eps',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='employee',
            name='include_employer_contribution',
            field=models.CharField(choices=[('Company Default', 'Company Default'), ('Yes', 'Yes'), ('No', 'No')], default='', max_length=20),
        ),
        migrations.AddField(
            model_name='employee',
            name='pf_status',
            field=models.CharField(choices=[('Opt In', 'Opt In'), ('Opt Out', 'Opt Out')], default='', max_length=10),
        ),
        migrations.AddField(
            model_name='employee',
            name='pf_wages_calculation',
            field=models.CharField(choices=[('Company Default', 'Company Default'), ('Under 15000', 'Under 15000'), ('No Limit', 'No Limit')], default='', max_length=20),
        ),
        migrations.AddField(
            model_name='employee',
            name='provident_fund_uan',
            field=models.CharField(default='', max_length=12, validators=[django.core.validators.RegexValidator(message='Provident Fund UAN must be a 12-digit number.', regex='^\\d{12}$')]),
        ),
        migrations.AddField(
            model_name='employee',
            name='pt_location',
            field=models.CharField(choices=[('State 01', 'State 01'), ('State 02', 'State 02')], default='', max_length=20),
        ),
        migrations.AddField(
            model_name='employee',
            name='pt_status',
            field=models.CharField(choices=[('Enabled', 'Enabled'), ('Disabled', 'Disabled')], default='', max_length=10),
        ),
        migrations.AlterField(
            model_name='step1sub3',
            name='pincode',
            field=models.CharField(default='', max_length=10, validators=[payrollapp.models.validate_pincode]),
        ),
    ]