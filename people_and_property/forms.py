from django import forms
from django.forms import ModelForm
from .models import Person, Email, Children, Address, Phone

# Forms
"""
Note that many of these forms are meant to be used in other applications. E.g, creating a client and
doing divorce papers will both use the 'CreatePerson' form. They are kept here for consistency.
"""


class CreatePerson(ModelForm):
    class Meta:
        model = Person
        fields = ['name_first', 'name_middle', 'name_last',
                  'gender', 'ssn', 'client', 'employee']


class CreateEmail(ModelForm):
    class Meta:
        model = Email
        fields = ['owner', 'address']


class CreatePhone(ModelForm):
    class Meta:
        model = Phone
        fields = ['owner', 'area_code', 'prefix', 'line_number', 'extension', 'fax']