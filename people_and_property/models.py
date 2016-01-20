from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
import uuid

# CONSTANTS
US_STATES = (
    ('AL', 'Alabama'),
    ('AK', 'Alaska'),

)

KY_COUNTIES = (
    ('Adair', 'Adair'),
    ('Allen', 'Allen'),
)

# Create your models here.


class Person(models.Model):
    """
    This class is for persons of whatever kind.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_date = models.DateTimeField(auto_now_add=True, null=True)
    updated_date = models.DateTimeField(auto_now=True, null=True)
    user = models.ForeignKey(User, null=True, related_name='person_info')
    name_first = models.CharField('First Name', max_length=100)
    name_middle = models.CharField('Middle Name', max_length=100, blank=True)
    name_last = models.CharField('Last Name', max_length=100)
    gender = models.CharField(max_length=30, null=True, choices=(('male', 'male'), ('female', 'female')))
    birthdate = models.DateField(null=True, blank=True)
    ssn = models.IntegerField('ssn', blank=True, null=True,
                              help_text='Type in your social security number without dashes.')
    client = models.BooleanField('client', default=False)  # True if client
    employee = models.BooleanField('employee', default=False)  # True if employee

    def __str__(self):
        if self.name_middle == '':
            return str(self.name_last) + ', ' + str(self.name_first)
        else:
            return str(self.name_last) + ', ' + str(self.name_first) + ' ' + str(self.name_middle)

    def get_absolute_url(self):
        return reverse('people_and_property:person-detail', kwargs={'pk': self.pk})


class Email(models.Model):
    """
    This class stores emails for people_and_property
    """
    EMAIL_TYPE = (
        ('work', 'work'),
        ('home', 'home'),
        ('other', 'other')
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(Person, related_name='email_set')
    address = models.EmailField()
    primary = models.NullBooleanField(help_text='Is this the primary email address you use?')
    type = models.CharField(max_length=25, choices=EMAIL_TYPE, null=True, blank=True)

    def __str__(self):
        return self.address

    def get_absolute_url(self):
        return reverse('people_and_property:email-detail', kwargs={'pk': self.pk})
    # TO DO: Add absolute url


class Children(models.Model):
    """
    This class stores information about children. Note that it is tied to the Person
    model both for parents and for the child
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    child = models.ForeignKey(Person, related_name='childhood_object')
    parents = models.ManyToManyField(Person, related_name='children_set')
    # TO DO: Add absolute url

class Address(models.Model):
    """
    This class stores addresses of whatever kind
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    residents = models.ManyToManyField(Person, related_name='address_set')
    street_address = models.CharField(max_length=90,
                                      help_text='What is the street number? For example, 271 W. Short St.')
    suite_number = models.CharField(blank=True, max_length=10)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=50, choices=US_STATES)
    zip = models.CharField(max_length=20, null=True)
    county = models.CharField(max_length=70, choices=KY_COUNTIES, blank=True)
    country = models.CharField(max_length=70, default='USA')
    confidential = models.BooleanField(help_text=('Is there some reason to keep the address secret from other ' +
                                                  'people involved in this case, for example, domestic violence?'),
                                       default=False)
    current = models.NullBooleanField(help_text='Is this a current address?', default=True)

    def __str__(self):
        if self.suite_number == '':
            return str(self.street_address) + ', ' + str(self.city) + ', ' + str(self.state)
        else:
            return (str(self.street_address) + ' ' + str(self.suite_number) + ', ' +
                    str(self.city) + ', ' + str(self.state) + ' ')

    def get_absolute_url(self):
        return reverse('people_and_property:address_detail', kwargs={'pk': self.pk})


class Phone(models.Model):
    """
    This class stores phone numbers of whatever kind
    """
    PHONE_TYPES = (
        ('home', 'home'),
        ('work', 'work'),
        ('cell', 'cell'),
        ('other', 'other')
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(Person, related_name='phone_set', null=True)
    # Note: on phone numbers, you may have to strip out any extra dots and dashes on the form side
    phone_number = models.CharField(max_length=20, help_text=('Enter your phone number.'))
    primary = models.NullBooleanField(default=True, help_text='Is this the best number to reach you?')
    extension = models.IntegerField(null=True, blank=True, help_text='Enter your extension if you have one.')
    type = models.CharField(max_length=20, choices=PHONE_TYPES, default='home')

    def __str__(self):
        if self.extension:
            return str(self.phone_number) + str(self.extension)
        else:
            return str(self.phone_number)

    def get_absolute_url(self):
        return reverse('people_and_property:phone_detail', kwargs={'pk': self.pk})


class Fax(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(Person, related_name='fax_set', null=True)
    phone_number = models.CharField(max_length=20, help_text='Enter the fax number')

    def __str__(self):
        return str(self.phone_number)

    def get_absolute_url(self):
        return reverse ('people_and_property:fax_detail', kwargs={'pk': self.pk})


# MARRIAGES/FAMILY


class Marriage(models.Model):
    """
    This class stores information about a marriage
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    spouses = models.ManyToManyField(Person, related_name='marriage_set_spouses')
    date_of_marriage = models.DateField(null=True)
    num_of_children = models.IntegerField(null=True)
    children_of_marriage = models.ManyToManyField(Person, blank=True,
                                                  related_name='marriage_set_children',
                                                  help_text='Children born during the marriage to the Wife')
    children_of_parties = models.ManyToManyField(Person, null=True,
                                                 blank=True,
                                                 related_name='children_of_parties',
                                                 help_text='Children born to the parties of the marriage')
    state = models.CharField(max_length=30, blank=True, null=True)
    county = models.CharField(max_length=30, blank=True, null=True)
    city = models.CharField(max_length=30, blank=True, null=True)


class DomesticViolenceCase(models.Model):
    """
    This class stores information about domestic violence cases
    TO DO: Move to divorce app
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    petitioner = models.ForeignKey(Person, related_name='petitioner')
    respondent = models.ForeignKey(Person, related_name='respondent')
    against = models.ManyToManyField(Person, related_name='against')  # Covers situation where dvo against both
    case_number = models.CharField(max_length=20)
    no_contact = models.BooleanField()
    expires = models.DateField()


class DomesticViolenceOrder(models.Model):
    """
    This class stores information about domestic violence orders

    TO DO: Move to divorce app
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    protected_parties = models.ManyToManyField(Person,
                                               related_name='protected_parties',
                                               help_text='People who are protected by the DVO')
    adverse_party = models.ForeignKey(Person, related_name='adverse_party',
                                      help_text='The party the DVO is against')
    expires = models.DateField(help_text='The date the DVO/EPO expires')
    no_contact = models.BooleanField(default=False, help_text='Does the Order prevent all contact?')


class Employment(models.Model):
    """
    This class stores employers' information. Note that this is a one to one relationships,
    so that, if there are multiple people that work in one place, there will be different
    entries for employers even though the employer might be the same in several cases
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    self_employed = models.BooleanField(default=False)
    employer_name = models.CharField(max_length=80,
                                     help_text='What is the name of the employer (e.g., Lexmark)?',
                                     null=True)
    employer_address = models.ForeignKey(Address, related_name='employer_address')
    type_of_work = models.CharField(max_length=100,
                                    help_text='What sort of work? For example, engineering, serving.')
    employee = models.ForeignKey(Person, related_name='employee_set')
    gross_monthly_income = models.DecimalField(help_text='Total amount of monthly income before taxes',
                                               decimal_places=2, max_digits=15)
    net_monthly_income = models.DecimalField(decimal_places=2, max_digits=15,
                                             help_text='Total amount of monthly income after taxes')
    address = models.ForeignKey(Address, related_name='address')
    fulltime = models.NullBooleanField(help_text='Is this a full time job?')


# ASSETS

class OwnershipInterest(models.Model):
    """
    This class represents an ownership interests for properties of whatever types.
    Each ownership interest is for a single person
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(Person, related_name='ownership_interest')
    percent_ownership = models.DecimalField(decimal_places=2, default=100.00, max_digits=15)


class Car(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ownership_interest = models.ManyToManyField(OwnershipInterest,
                                                help_text='Whose name is on the title?')
    make = models.CharField(help_text='What is the make of the car (e.g., Toyata, GM',
                            max_length=50)
    model = models.CharField(help_text='What is the model of the care (e.g, Camry, Focus)',
                             max_length=50)
    primary_driver = models.ForeignKey(Person, related_name='primary_driver',
                                       help_text='Who is the primary driver of the car?')
    nada_value = models.DecimalField(null=True, decimal_places=2, max_digits=15,
                                     help_text=('What is the NADA value of the car? You can find it on' +
                                                'www.nadaguides.com'))


class CarDebt(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    car = models.ForeignKey(Car, related_name='car')
    total_debt = models.DecimalField(decimal_places=2, max_digits=15)
    monthly_payment = models.DecimalField(decimal_places=2, max_digits=15)
    lender = models.CharField(help_text='Who is the lender of the debt on the car',
                              max_length=50)


class BankAccount(models.Model):
    ACCOUNT_TYPE = (
        ('checking', 'Checking Account'),
        ('savings', 'Savings Account'),
        ('cd', 'Certificate of Deposit (CD)'),
        ('money_market', 'Money Market'),
        ('other', 'Other')
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ownership_interests = models.ManyToManyField(OwnershipInterest, related_name='ownership_of_bank_account',
                                              help_text='Whose name is on the account?')
    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPE)
    current_balance = models.DecimalField(decimal_places=2, null=True, max_digits=15)
    date_balance_checked = models.DateField(help_text='What date was the balance last checked?', null=True)
    account_number = models.CharField(max_length=30,
                                      help_text='What is the account number for the bank account?')


class InvestmentAccount(models.Model):
    INVESTMENT_TYPE = (
        ('stock', 'Stock'),
        ('bond', 'Bond'),
        ('portfolio', 'Portfolio'),
        ('mutual fund', 'Mutual Fund'),
        ('other', 'Other')
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=40, help_text='What is the account called?')
    institution = models.CharField(max_length=40, help_text='With what institution do you have the investment?')
    ownership_interests = models.ManyToManyField(OwnershipInterest, related_name='investment_accounts',
                                              help_text='Whose name is on the account?')
    account_type = models.CharField(max_length=20, choices=INVESTMENT_TYPE)
    current_value = models.DecimalField(decimal_places=2, max_digits=15,
                                        help_text=('What is the current value of the investment?'))
    valuation_date = models.DateField(help_text='What date did you last check the value of the investment?')
    account_number = models.CharField(max_length=30,
                                      help_text='What is the account number for the investment account?')


class RetirementBenefits(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=30,
                            help_text='What is the name of the retirement benefit?')
    participant = models.ForeignKey(Person, related_name='participant')
    contributory = models.BooleanField(help_text='Is the retirement account contributory?')
    vested = models.BooleanField(help_text='Is the retirement account vested?')
    current_value = models.DecimalField(decimal_places=2, max_digits=15,
                                        help_text='What is the current value of the retirement benefit?')
    valuation_date = models.DateField(help_text='What was the last date you checked the value?')
    in_payout_status = models.BooleanField(help_text='Is the retirement benefit currently in payout status?')
    account_number = models.CharField(max_length=30,
                                      help_text='What is the account number for the retirement benefit?')


class LifeInsurance(models.Model):
    INSURANCE_TYPE = (
        ('term', 'Term'),
        ('whole', 'Whole Life')
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    institution = models.CharField(max_length=30,
                                   help_text='What is the institution for the life insurance?')
    insured_party = models.ForeignKey(Person, related_name='insured_party',
                                      help_text='Who is the party insured by the life insurance?')
    owner = models.ForeignKey(Person, related_name='owner_of_life_insurance',
                              help_text='Who owns the policy?')
    beneficiaries = models.ForeignKey(Person, related_name='insurance_beneficiary',
                                      help_text='Who is named as the beneficiary?')
    cash_surrender_value = models.DecimalField(decimal_places=2, max_digits=15,
                                               help_text=('What is the cash surrender value of the policy?'
                                                          + '(If term, put 0'))
    date_of_valuation = models.DateField(help_text='What was the date you checked the cash surrender value?')


class BusinessInterest(models.Model):
    BUSINESS_TYPE = (
        ('corporation', 'Corporation'),
        ('llc', 'LLC or PLLC'),
        ('sole proprietorship', 'Sole Proprietorship'),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=30, help_text='What is the name of the business?')
    description = models.TextField(help_text='Describe the business.')
    value_known = models.NullBooleanField(help_text='Do you know the value of the business?',
                                          null=True)
    current_value = models.DecimalField(decimal_places=2, null=True, max_digits=15)
    valuation_date = models.DateField(help_text='What is the date the valuation was done?',
                                      null=True)
    ownership_interests = models.ManyToManyField(OwnershipInterest, related_name='business_interests')


class BusinessLoans(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    business_for_loan = models.ForeignKey(BusinessInterest,
                                          related_name='business_loans',
                                          help_text='Which business is this loan connected to?')
    secured = models.NullBooleanField(help_text='Is this loan secured?')
    lender = models.CharField(max_length=35,
                                   help_text='Who is the lendor?')
    balance = models.DecimalField(decimal_places=2, max_digits=15,
                                  help_text='What is the current balance of the loan')
    date_of_balance = models.DateField(help_text='What date was the balance of the loan last checked?')


class RealProperty(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owners = models.ManyToManyField(Person, related_name='real_property_owned',
                                    help_text='Whose name is on the deed?')
    street_number = models.CharField(max_length=10)
    street_name = models.CharField(max_length=20)
    suite_number = models.CharField(max_length=10, blank=True,
                                    help_text='The suite or apartment number')
    city = models.CharField(max_length=30)
    state = models.CharField(choices=US_STATES, max_length=25)
    country = models.CharField(default='USA', max_length=25)
    fair_market_value = models.DecimalField(decimal_places=2, null=True, max_digits=15)
    pva_value = models.DecimalField(decimal_places=2, null=True, max_digits=15)
    valuation_date = models.DateField(help_text='What was the date of the valuation was done?')


class Mortgages(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    debtors = models.ManyToManyField(Person, help_text='Whose name is on the mortgage?',
                                     related_name='mortgage_debt')
    lender = models.CharField(help_text='Who is the lender?', max_length=30)
    property = models.ForeignKey(RealProperty, related_name='mortgages')
    payoff_amount = models.DecimalField(help_text='What is the payoff amount?', max_digits=15,
                                        decimal_places=2)
    total_balance = models.DecimalField(help_text='What is the total balance?', max_digits=15,
                                        decimal_places=2)
    monthly_payment = models.DecimalField(decimal_places=2, max_digits=15)


class PersonalProperty(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=40,
                            help_text='What is the item called?')
    description = models.TextField(help_text='Describe the item')
    value = models.DecimalField(help_text='What is the value of the item?', max_digits=15, decimal_places=2)
    valuation_date = models.DateField('When was the item evaluated?', blank=True, null=True)
    amount_owed = models.DecimalField(help_text='What amount is owed on the item?', max_digits=15,
                                      decimal_places=2)


class Debts(models.Model):
    """
    This class is for debts other than car loans, mortgages, and debts secured by
    personal property
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    lender = models.CharField(max_length=50, help_text='Who is the current lender for the loan?')
    debtors = models.ManyToManyField(Person, related_name='debt_set')
    current_balance = models.DecimalField(decimal_places=2, max_digits=15,
                                          help_text='What is the current balance?')
    balance_date = models.DateTimeField(help_text='What date did you last check the balance?')
    monthly_payment = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=15,
                                          help_text='What is the total monthly payment?')
