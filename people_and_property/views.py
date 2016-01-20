from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.views.generic import DetailView
from django.views.generic.edit import UpdateView, CreateView
from django.contrib.auth.mixins import PermissionRequiredMixin

import logging

from .models import Person, Email, Phone, Fax, Address

# Logging settings

logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')
logging.debug('Start of people_and_property/views.py')

# Create your views here.

# PERSON views

class PersonCreate(PermissionRequiredMixin, CreateView):
    """
    This view is for staff members to create new person objects.
    """
    template_name = 'people_and_property/person_create.html'
    model = Person
    context_object_name = 'person'
    permission_required = 'people_and_property.can_add_person'
    fields = ['user', 'name_first', 'name_middle', 'name_last', 'gender', 'birthdate', 'ssn', 'client']


class PersonDetail(PermissionRequiredMixin, DetailView):
    """
    This view displays details about persons. Note that it should not be used for clients,
    since there will be different permission requirements for it. Plus it uses the client
    portal base.
    """
    model = Person
    template_name = "people_and_property/person_detail.html"
    context_object_name = 'person'
    permission_required = 'people_and_property.can_change_person'


class PersonUpdate(PermissionRequiredMixin, UpdateView):
    """
    This view allows you to update a person object. Note that it should not be used for clients,
    since there are different permissions that will need to be set. Plus, the template uses
    the client portal.
    """
    model = Person
    template_name = "people_and_property/person_update.html"
    context_object_name = 'person'
    fields = ['name_first', 'name_middle', 'name_last', 'gender', 'birthdate', 'ssn', 'client']
    permission_required = 'people_and_property.can_change_person'

# TO DO: Create a generic template that renders the form, and do an editing page for
# each of the major categories in people_and_property


class EmailCreate(PermissionRequiredMixin, CreateView):
    """
    This view allows staff to create email objects
    """
    model = Email
    fields = ['owner', 'address', 'primary']
    template_name = 'people_and_property/generic_create.html'
    permission_required = 'people_and_property.can_add_email'

    def get_context_data(self, **kwargs):
        """
        This should add in the url for the template to send the data to.
        """
        context = super(EmailCreate, self).get_context_data(**kwargs)
        context['name_of_object'] = 'Email' # This tells the template what it is that we're editing
        context['action_html'] = reverse('people_and_property:email-create')
        return context


class EmailDetail(PermissionRequiredMixin, DetailView):
    """
    This is for employees to view the detail of emails
    """
    model = Email
    template_name = 'people_and_property/email_detail.html'
    context_object_name = 'email' # Rather than email - that way the template can have a link to its absolute url
    permission_required = 'people_and_property.can_change_email'


class EmailUpdate(PermissionRequiredMixin, UpdateView):
    """
    This is for employees to update an email
    """
    model = Email
    fields = ['owner', 'address', 'primary']
    template_name = 'people_and_property/generic_update.html'
    permission_required = 'people_and_property.can_add_email'

    def get_context_data(self, **kwargs):
        logging.debug ('About to try to set context data for EmailUpdate page')
        logging.debug ('action_html to be set to %s' %
                       reverse('people_and_property:email_update', kwargs={'pk': self.object.id}))
        context = super(EmailUpdate, self).get_context_data(**kwargs)
        context['name_of_object'] = 'Email'
        context['action_html'] = reverse('people_and_property:email_update', kwargs={'pk': self.object.id})
        return context

class PhoneDetail(PermissionRequiredMixin, DetailView):
    """
    This is for employees to view the details about a phone
    """
    model = Phone
    template_name = 'people_and_property/phone_detail.html'
    context_object_name = 'phone'
    permission_required = 'people_and_property.can_change_phone'


class PhoneCreate(PermissionRequiredMixin, CreateView):
    """
    This is for employees to create a phone number object
    """
    model = Phone
    template_name = 'people_and_property/generic_create.html'
    fields = ['owner', 'phone_number', 'extension', 'primary', 'type']
    permission_required = 'people_and_property.can_add_phone'

    def get_context_data(self, **kwargs):
        """
        This should add in the url for the template to send the data to.
        """
        context = super(PhoneCreate, self).get_context_data(**kwargs)
        context['name_of_object'] = 'Phone'  # This tells the template what it is that we're editing
        context['action_html'] = reverse('people_and_property:phone_create')
        return context


class PhoneUpdate(PermissionRequiredMixin, UpdateView):
    """
    This is for employees to update phone objects
    """
    model = Phone
    template_name = 'people_and_property/generic_update.html'
    fields = ['owner', 'phone_number', 'extension', 'primary', 'type']
    permission_required = 'people_and_property.can_change_phone'

    def get_context_data(self, **kwargs):
        context = super(PhoneUpdate, self).get_context_data(**kwargs)
        context['name_of_object'] = 'Phone'
        context['action_html'] = reverse('people_and_property:phone_update', kwargs={'pk': self.object.id})
        return context


class FaxCreate(PermissionRequiredMixin, CreateView):
    """
    This is for employees to create fax numbers/objects
    """
    model = Fax
    template_name = 'people_and_property/generic_create.html'
    fields = ['owner', 'phone_number']
    permission_required = 'people_and_property.can_change_fax'

    def get_context_data(self, **kwargs):
        context = super(FaxCreate, self).get_context_data(**kwargs)
        context['name_of_object'] = 'Fax' # This tells the template what it is that we're editing
        context['action_html'] = reverse('people_and_property:fax_create')
        return context


class FaxDetail(PermissionRequiredMixin, DetailView):
    """
    This is for employees to view the details of a fax number
    """
    model = Fax
    template_name = 'people_and_property/fax_detail.html'
    context_object_name = 'fax'
    permission_required = 'people_and_property.can_change_fax'


class FaxUpdate(PermissionRequiredMixin, UpdateView):
    """
    This is for employees to update fax numbers
    """
    model = Fax
    template_name = 'people_and_property/generic_update.html'
    fields = ['owner', 'phone_number']
    permission_required = 'people_and_property.can_change_fax'

    def get_context_data(self, **kwargs):
        context = super(FaxUpdate, self).get_context_data(**kwargs)
        context['name_of_object'] = 'Fax'
        context['action_html'] = reverse('people_and_property:fax_update', kwargs={'pk': self.object.id})
        return context


class AddressDetail(PermissionRequiredMixin, DetailView):
    """
    This is for employees to view details about an address
    """
    model = Address
    template_name = 'people_and_property/address_detail.html'
    permission_required = 'people_and_property.can_change_address'
    context_object_name = 'address'


class AddressCreate(PermissionRequiredMixin, CreateView):
    """
    This is for staff to create address objects
    """
    model = Address
    template_name = 'people_and_property/generic_create.html'
    permission_required = 'people_and_property.can_add_address'
    fields = ['residents', 'street_address', 'suite_number', 'city', 'state',
              'zip', 'county', 'country', 'confidential', 'current']

    def get_context_data(self, **kwargs):
        context = super(AddressCreate, self).get_context_data(**kwargs)
        context['name_of_object'] = 'Address'
        context['action_html'] = reverse('people_and_property:address_create')
        return context


class AddressUpdate(PermissionRequiredMixin, UpdateView):
    """
    This class is for staff to update address objects
    """
    model = Address
    template_name = 'people_and_property/generic_update.html'
    fields = ['residents', 'street_address', 'suite_number', 'city', 'state',
              'zip', 'county', 'country', 'confidential', 'current']
    permission_required = 'people_and_property.can_change_address'

    def get_context_data(self, **kwargs):
        context = super(AddressUpdate, self).get_context_data(**kwargs)
        context['name_of_object'] = 'Address'
        context['action_html'] = reverse('people_and_property:address_update', kwargs={'pk': self.object.id})
        return context