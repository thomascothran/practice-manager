from django import forms
from phonenumber_field.formfields import PhoneNumberField
from django.forms import ModelForm
from .models import Case


# Create Client Form

class CreateNewClient(forms.Form):
    """
    This form will be used to create new clients.

    TO DO: Move to using a multi-page wizard that incorporates the forms from other
    apps (e.g., the people_and_property apps). Reason: because if you change the models
    and forms in those apps, you want the creation of new clients to not be broken by
    the changes.
    """

    name_first = forms.CharField(max_length=60, label='First name')
    name_middle = forms.CharField(max_length=60, label='Middle name', required=False)
    name_last = forms.CharField(max_length=60, label='Last name')
    gender = forms.ChoiceField(choices=(('male', 'male'), ('female', 'female')))
    email = forms.EmailField(required=False)
    phone = PhoneNumberField(required=False)


class CreateNewCase(ModelForm):
    """
    This form will be used to create a new case, after the client has been created.
    """
    class Meta:
        model = Case
        fields = ['type_of_case', 'date_started', 'client',]


class CaseFilter(forms.Form):
    """
    This form will be used to filter forms on the index page.
    """
    status = forms.ChoiceField(required=False,
                               choices=(('', ''),
                                        ('open', 'open'),
                                        ('closed except payment', 'Closed case, payment pending'),
                                        ('closed', 'paid and closed'),))
    first_name = forms.CharField(max_length=60, label='First Name', required=False)
    last_name = forms.CharField(max_length=60, label='Last Name', required=False)


class ClientFilter(forms.Form):
    """
    This filter is used to sort through clients
    """
    first_name = forms.CharField(max_length=100, label='First Name', required=False)
    last_name = forms.CharField(max_length=100, label='Last Name')

