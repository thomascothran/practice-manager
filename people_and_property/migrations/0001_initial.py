# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-09 21:18
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('street_address', models.CharField(help_text='What is the street number? For example, 271 W. Short St.', max_length=90)),
                ('suite_number', models.CharField(blank=True, max_length=10)),
                ('city', models.CharField(max_length=100)),
                ('state', models.CharField(choices=[('AL', 'Alabama'), ('AK', 'Alaska')], max_length=50)),
                ('zip', models.CharField(max_length=20, null=True)),
                ('county', models.CharField(blank=True, choices=[('Adair', 'Adair'), ('Allen', 'Allen')], max_length=70)),
                ('country', models.CharField(default='USA', max_length=70)),
                ('confidential', models.BooleanField(default=False, help_text='Is there some reason to keep the address secret from other people involved in this case, for example, domestic violence?')),
                ('current', models.NullBooleanField(default=True, help_text='Is this a current address?')),
            ],
        ),
        migrations.CreateModel(
            name='BankAccount',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('account_type', models.CharField(choices=[('checking', 'Checking Account'), ('savings', 'Savings Account'), ('cd', 'Certificate of Deposit (CD)'), ('money_market', 'Money Market'), ('other', 'Other')], max_length=20)),
                ('current_balance', models.DecimalField(decimal_places=2, max_digits=15, null=True)),
                ('date_balance_checked', models.DateField(help_text='What date was the balance last checked?', null=True)),
                ('account_number', models.CharField(help_text='What is the account number for the bank account?', max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='BusinessInterest',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(help_text='What is the name of the business?', max_length=30)),
                ('description', models.TextField(help_text='Describe the business.')),
                ('value_known', models.NullBooleanField(help_text='Do you know the value of the business?')),
                ('current_value', models.DecimalField(decimal_places=2, max_digits=15, null=True)),
                ('valuation_date', models.DateField(help_text='What is the date the valuation was done?', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='BusinessLoans',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('secured', models.NullBooleanField(help_text='Is this loan secured?')),
                ('lender', models.CharField(help_text='Who is the lendor?', max_length=35)),
                ('balance', models.DecimalField(decimal_places=2, help_text='What is the current balance of the loan', max_digits=15)),
                ('date_of_balance', models.DateField(help_text='What date was the balance of the loan last checked?')),
                ('business_for_loan', models.ForeignKey(help_text='Which business is this loan connected to?', on_delete=django.db.models.deletion.CASCADE, related_name='business_loans', to='people_and_property.BusinessInterest')),
            ],
        ),
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('make', models.CharField(help_text='What is the make of the car (e.g., Toyata, GM', max_length=50)),
                ('model', models.CharField(help_text='What is the model of the care (e.g, Camry, Focus)', max_length=50)),
                ('nada_value', models.DecimalField(decimal_places=2, help_text='What is the NADA value of the car? You can find it onwww.nadaguides.com', max_digits=15, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='CarDebt',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('total_debt', models.DecimalField(decimal_places=2, max_digits=15)),
                ('monthly_payment', models.DecimalField(decimal_places=2, max_digits=15)),
                ('lender', models.CharField(help_text='Who is the lender of the debt on the car', max_length=50)),
                ('car', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='car', to='people_and_property.Car')),
            ],
        ),
        migrations.CreateModel(
            name='Children',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Debts',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('lender', models.CharField(help_text='Who is the current lender for the loan?', max_length=50)),
                ('current_balance', models.DecimalField(decimal_places=2, help_text='What is the current balance?', max_digits=15)),
                ('balance_date', models.DateTimeField(help_text='What date did you last check the balance?')),
                ('monthly_payment', models.DecimalField(blank=True, decimal_places=2, help_text='What is the total monthly payment?', max_digits=15, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='DomesticViolenceCase',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('case_number', models.CharField(max_length=20)),
                ('no_contact', models.BooleanField()),
                ('expires', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='DomesticViolenceOrder',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('expires', models.DateField(help_text='The date the DVO/EPO expires')),
                ('no_contact', models.BooleanField(default=False, help_text='Does the Order prevent all contact?')),
            ],
        ),
        migrations.CreateModel(
            name='Email',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('address', models.EmailField(max_length=254)),
                ('primary', models.NullBooleanField(help_text='Is this the primary email address you use?')),
                ('type', models.CharField(blank=True, choices=[('work', 'work'), ('home', 'home'), ('other', 'other')], max_length=25, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Employment',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('self_employed', models.BooleanField(default=False)),
                ('employer_name', models.CharField(help_text='What is the name of the employer (e.g., Lexmark)?', max_length=80, null=True)),
                ('type_of_work', models.CharField(help_text='What sort of work? For example, engineering, serving.', max_length=100)),
                ('gross_monthly_income', models.DecimalField(decimal_places=2, help_text='Total amount of monthly income before taxes', max_digits=15)),
                ('net_monthly_income', models.DecimalField(decimal_places=2, help_text='Total amount of monthly income after taxes', max_digits=15)),
                ('fulltime', models.NullBooleanField(help_text='Is this a full time job?')),
                ('address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='address', to='people_and_property.Address')),
            ],
        ),
        migrations.CreateModel(
            name='Fax',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('phone_number', models.CharField(help_text='Enter the fax number', max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='InvestmentAccount',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(help_text='What is the account called?', max_length=40)),
                ('institution', models.CharField(help_text='With what institution do you have the investment?', max_length=40)),
                ('account_type', models.CharField(choices=[('stock', 'Stock'), ('bond', 'Bond'), ('portfolio', 'Portfolio'), ('mutual fund', 'Mutual Fund'), ('other', 'Other')], max_length=20)),
                ('current_value', models.DecimalField(decimal_places=2, help_text='What is the current value of the investment?', max_digits=15)),
                ('valuation_date', models.DateField(help_text='What date did you last check the value of the investment?')),
                ('account_number', models.CharField(help_text='What is the account number for the investment account?', max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='LifeInsurance',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('institution', models.CharField(help_text='What is the institution for the life insurance?', max_length=30)),
                ('cash_surrender_value', models.DecimalField(decimal_places=2, help_text='What is the cash surrender value of the policy?(If term, put 0', max_digits=15)),
                ('date_of_valuation', models.DateField(help_text='What was the date you checked the cash surrender value?')),
            ],
        ),
        migrations.CreateModel(
            name='Marriage',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('date_of_marriage', models.DateField(null=True)),
                ('num_of_children', models.IntegerField(null=True)),
                ('state', models.CharField(blank=True, max_length=30, null=True)),
                ('county', models.CharField(blank=True, max_length=30, null=True)),
                ('city', models.CharField(blank=True, max_length=30, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Mortgages',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('lender', models.CharField(help_text='Who is the lender?', max_length=30)),
                ('payoff_amount', models.DecimalField(decimal_places=2, help_text='What is the payoff amount?', max_digits=15)),
                ('total_balance', models.DecimalField(decimal_places=2, help_text='What is the total balance?', max_digits=15)),
                ('monthly_payment', models.DecimalField(decimal_places=2, max_digits=15)),
            ],
        ),
        migrations.CreateModel(
            name='OwnershipInterest',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('percent_ownership', models.DecimalField(decimal_places=2, default=100.0, max_digits=15)),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_date', models.DateTimeField(auto_now=True, null=True)),
                ('name_first', models.CharField(max_length=100, verbose_name='First Name')),
                ('name_middle', models.CharField(blank=True, max_length=100, verbose_name='Middle Name')),
                ('name_last', models.CharField(max_length=100, verbose_name='Last Name')),
                ('gender', models.CharField(choices=[('male', 'male'), ('female', 'female')], max_length=30, null=True)),
                ('birthdate', models.DateField(blank=True, null=True)),
                ('ssn', models.IntegerField(blank=True, help_text='Type in your social security number without dashes.', null=True, verbose_name='ssn')),
                ('client', models.BooleanField(default=False, verbose_name='client')),
                ('employee', models.BooleanField(default=False, verbose_name='employee')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='person_info', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PersonalProperty',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(help_text='What is the item called?', max_length=40)),
                ('description', models.TextField(help_text='Describe the item')),
                ('value', models.DecimalField(decimal_places=2, help_text='What is the value of the item?', max_digits=15)),
                ('valuation_date', models.DateField(blank=True, null=True, verbose_name='When was the item evaluated?')),
                ('amount_owed', models.DecimalField(decimal_places=2, help_text='What amount is owed on the item?', max_digits=15)),
            ],
        ),
        migrations.CreateModel(
            name='Phone',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('phone_number', models.CharField(help_text='Enter your phone number.', max_length=20)),
                ('primary', models.NullBooleanField(default=True, help_text='Is this the best number to reach you?')),
                ('extension', models.IntegerField(blank=True, help_text='Enter your extension if you have one.', null=True)),
                ('type', models.CharField(choices=[('home', 'home'), ('work', 'work'), ('cell', 'cell'), ('other', 'other')], default='home', max_length=20)),
                ('owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='phone_set', to='people_and_property.Person')),
            ],
        ),
        migrations.CreateModel(
            name='RealProperty',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('street_number', models.CharField(max_length=10)),
                ('street_name', models.CharField(max_length=20)),
                ('suite_number', models.CharField(blank=True, help_text='The suite or apartment number', max_length=10)),
                ('city', models.CharField(max_length=30)),
                ('state', models.CharField(choices=[('AL', 'Alabama'), ('AK', 'Alaska')], max_length=25)),
                ('country', models.CharField(default='USA', max_length=25)),
                ('fair_market_value', models.DecimalField(decimal_places=2, max_digits=15, null=True)),
                ('pva_value', models.DecimalField(decimal_places=2, max_digits=15, null=True)),
                ('valuation_date', models.DateField(help_text='What was the date of the valuation was done?')),
                ('owners', models.ManyToManyField(help_text='Whose name is on the deed?', related_name='real_property_owned', to='people_and_property.Person')),
            ],
        ),
        migrations.CreateModel(
            name='RetirementBenefits',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(help_text='What is the name of the retirement benefit?', max_length=30)),
                ('contributory', models.BooleanField(help_text='Is the retirement account contributory?')),
                ('vested', models.BooleanField(help_text='Is the retirement account vested?')),
                ('current_value', models.DecimalField(decimal_places=2, help_text='What is the current value of the retirement benefit?', max_digits=15)),
                ('valuation_date', models.DateField(help_text='What was the last date you checked the value?')),
                ('in_payout_status', models.BooleanField(help_text='Is the retirement benefit currently in payout status?')),
                ('account_number', models.CharField(help_text='What is the account number for the retirement benefit?', max_length=30)),
                ('participant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='participant', to='people_and_property.Person')),
            ],
        ),
        migrations.AddField(
            model_name='ownershipinterest',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ownership_interest', to='people_and_property.Person'),
        ),
        migrations.AddField(
            model_name='mortgages',
            name='debtors',
            field=models.ManyToManyField(help_text='Whose name is on the mortgage?', related_name='mortgage_debt', to='people_and_property.Person'),
        ),
        migrations.AddField(
            model_name='mortgages',
            name='property',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mortgages', to='people_and_property.RealProperty'),
        ),
        migrations.AddField(
            model_name='marriage',
            name='children_of_marriage',
            field=models.ManyToManyField(blank=True, help_text='Children born during the marriage to the Wife', related_name='marriage_set_children', to='people_and_property.Person'),
        ),
        migrations.AddField(
            model_name='marriage',
            name='children_of_parties',
            field=models.ManyToManyField(blank=True, help_text='Children born to the parties of the marriage', null=True, related_name='children_of_parties', to='people_and_property.Person'),
        ),
        migrations.AddField(
            model_name='marriage',
            name='spouses',
            field=models.ManyToManyField(related_name='marriage_set_spouses', to='people_and_property.Person'),
        ),
        migrations.AddField(
            model_name='lifeinsurance',
            name='beneficiaries',
            field=models.ForeignKey(help_text='Who is named as the beneficiary?', on_delete=django.db.models.deletion.CASCADE, related_name='insurance_beneficiary', to='people_and_property.Person'),
        ),
        migrations.AddField(
            model_name='lifeinsurance',
            name='insured_party',
            field=models.ForeignKey(help_text='Who is the party insured by the life insurance?', on_delete=django.db.models.deletion.CASCADE, related_name='insured_party', to='people_and_property.Person'),
        ),
        migrations.AddField(
            model_name='lifeinsurance',
            name='owner',
            field=models.ForeignKey(help_text='Who owns the policy?', on_delete=django.db.models.deletion.CASCADE, related_name='owner_of_life_insurance', to='people_and_property.Person'),
        ),
        migrations.AddField(
            model_name='investmentaccount',
            name='ownership_interests',
            field=models.ManyToManyField(help_text='Whose name is on the account?', related_name='investment_accounts', to='people_and_property.OwnershipInterest'),
        ),
        migrations.AddField(
            model_name='fax',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='fax_set', to='people_and_property.Person'),
        ),
        migrations.AddField(
            model_name='employment',
            name='employee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='employee_set', to='people_and_property.Person'),
        ),
        migrations.AddField(
            model_name='employment',
            name='employer_address',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='employer_address', to='people_and_property.Address'),
        ),
        migrations.AddField(
            model_name='email',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='email_set', to='people_and_property.Person'),
        ),
        migrations.AddField(
            model_name='domesticviolenceorder',
            name='adverse_party',
            field=models.ForeignKey(help_text='The party the DVO is against', on_delete=django.db.models.deletion.CASCADE, related_name='adverse_party', to='people_and_property.Person'),
        ),
        migrations.AddField(
            model_name='domesticviolenceorder',
            name='protected_parties',
            field=models.ManyToManyField(help_text='People who are protected by the DVO', related_name='protected_parties', to='people_and_property.Person'),
        ),
        migrations.AddField(
            model_name='domesticviolencecase',
            name='against',
            field=models.ManyToManyField(related_name='against', to='people_and_property.Person'),
        ),
        migrations.AddField(
            model_name='domesticviolencecase',
            name='petitioner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='petitioner', to='people_and_property.Person'),
        ),
        migrations.AddField(
            model_name='domesticviolencecase',
            name='respondent',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='respondent', to='people_and_property.Person'),
        ),
        migrations.AddField(
            model_name='debts',
            name='debtors',
            field=models.ManyToManyField(related_name='debt_set', to='people_and_property.Person'),
        ),
        migrations.AddField(
            model_name='children',
            name='child',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='childhood_object', to='people_and_property.Person'),
        ),
        migrations.AddField(
            model_name='children',
            name='parents',
            field=models.ManyToManyField(related_name='children_set', to='people_and_property.Person'),
        ),
        migrations.AddField(
            model_name='car',
            name='ownership_interest',
            field=models.ManyToManyField(help_text='Whose name is on the title?', to='people_and_property.OwnershipInterest'),
        ),
        migrations.AddField(
            model_name='car',
            name='primary_driver',
            field=models.ForeignKey(help_text='Who is the primary driver of the car?', on_delete=django.db.models.deletion.CASCADE, related_name='primary_driver', to='people_and_property.Person'),
        ),
        migrations.AddField(
            model_name='businessinterest',
            name='ownership_interests',
            field=models.ManyToManyField(related_name='business_interests', to='people_and_property.OwnershipInterest'),
        ),
        migrations.AddField(
            model_name='bankaccount',
            name='ownership_interests',
            field=models.ManyToManyField(help_text='Whose name is on the account?', related_name='ownership_of_bank_account', to='people_and_property.OwnershipInterest'),
        ),
        migrations.AddField(
            model_name='address',
            name='residents',
            field=models.ManyToManyField(related_name='address_set', to='people_and_property.Person'),
        ),
    ]
