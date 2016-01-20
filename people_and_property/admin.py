from django.contrib import admin
from .models import Phone, Person, Email, Children, Address, Employment, OwnershipInterest, \
    Car, CarDebt, BankAccount, InvestmentAccount, RetirementBenefits, LifeInsurance, BusinessInterest, \
    BusinessLoans, RealProperty, Mortgages, PersonalProperty, Debts

# Register your models here.
admin.site.register(Phone)
admin.site.register(Person)
admin.site.register(Email)
admin.site.register(Children)
admin.site.register(Address)
admin.site.register(Employment)
admin.site.register(OwnershipInterest)
admin.site.register(Car)
admin.site.register(CarDebt)
admin.site.register(BankAccount)
admin.site.register(InvestmentAccount)
admin.site.register(RetirementBenefits)
admin.site.register(LifeInsurance)
admin.site.register(BusinessInterest)
admin.site.register(BusinessLoans)
admin.site.register(RealProperty)
admin.site.register(Mortgages)
admin.site.register(PersonalProperty)
admin.site.register(Debts)
