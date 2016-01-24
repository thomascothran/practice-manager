from django.shortcuts import render
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import UserPassesTestMixin

from .models import Case
from people_and_property.models import Person, Address, Phone, Email
import case_manager.forms

import logging
import uuid

# Start logging
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')
logging.debug('Start of case_manager/views.py')

# TO DO: Restrict page views to those who have permissions


def user_is_staff(user):
    """
    This function is to be used with the user_passes_test decorator
    to limit viewing the page to users who are logged in
    """
    return user.is_staff == True and user.is_active == True


@user_passes_test(user_is_staff)
def IndexView(request):

    """
    This class is the homepage for case management.
    It should display cases and allow you to select them.
    """
    logging.debug('Entered case_manager.views.IndexView')
    # Set default context
    case_list = Case.objects.filter(status='open').order_by('-client') # By default, send all open cases
    context = {'case_list': case_list,
               'case_filter': case_manager.forms.CaseFilter,
              }

    # TO DO: If no post data,show all open cases by default
    if request.method != 'POST':
        logging.debug('request.method != POST, putting together index page.')
        return render(request, 'case_manager/index.html', context)

    # TO DO: Process POST data
    elif request.method == 'POST':
        logging.debug('request.method == POST, about to process post data.')
        post_data = case_manager.forms.CaseFilter(request.POST)
        logging.debug('created dict (post_data) for POST data')
        logging.debug("Post data validated? %s" % (str(post_data.is_valid())))

        # If POST data valid, return a page with filtered data
        if post_data.is_valid():
            logging.debug('Post data validated. About to process')
            logging.debug('There are %s items in cleaned_data:' %
                          (len(post_data.cleaned_data)))
            for k, v in post_data.cleaned_data.items():
                logging.debug('Key: %s, Value: %s' % (k, v))

            # Set filters
            client_name_first_filter = post_data.cleaned_data['first_name']
            client_name_last_filter = post_data.cleaned_data['last_name']
            status_filter = post_data.cleaned_data['status']

            # Apply filters
            case_list = Case.objects.all() # Selects all cases (not just open cass)
            logging.debug('Set case_list to all cases, about to filter')

            # Apply name filters (if any)
            if client_name_first_filter != '':
                case_list = case_list.filter(client__name_first__icontains=client_name_first_filter)

            if client_name_last_filter != '':
                case_list = case_list.filter(client__name_last__icontains=client_name_last_filter)

            if status_filter != '':
                logging.debug("Status filter != '', about to apply status filter")
                case_list = case_list.filter(status=status_filter)


            # Change context to reflect filtering
            context['case_list'] = case_list


            # Add notifications
            return render(request, 'case_manager/index.html', context)

        # TO DO: If data not validated, need to return data with notices.
        # How to do this is in the docs
        else:
            logging.error('Form data not validated')
            logging.debug('There are %s items in request.POST' % (len(request.POST)))
            logging.debug('Post data includes:')
            post_data = request.POST
            for k, v in post_data.items():
                logging.debug('Key: %s, Value: %s' % (k, v))

            # Build context
            context = {'case_filter': case_manager.forms.CaseFilter(request.POST),
                       # 'case_list': Case.objects.all(),
                       }
            return render(request, 'case_manager/index.html', context)


@user_passes_test(user_passes_test)
def CreateNewClient(request):
    """
    This view creates a new client. It displays the form for the creation
    of a client, and it also processes the post data.

    TO DO: Replace this with a more "modular" version that uses formtools
    to create a multipage form with optional parts
    """
    logging.debug('Entered case_manager.views.CreateNewClient')

    # Figure out whether there's post data. If no post data, show
    # a the form. If post data, process the data.

    # No post data, display form
    if request.method != 'POST':
        """ Display form and render to template
        """
        form = case_manager.forms.CreateNewClient
        context = {'form': form}
        return render(request, template_name='case_manager/create-new-client.html', context=context)

    # Post data, process post data to create new case
    elif request.method == 'POST':
        ''' Process results '''
        form_data = case_manager.forms.CreateNewClient(request.POST)
        # Check to see if the form data is valid
        if form_data.is_valid():
            # Set cleaned_data variable pointing to cleaned data
            cleaned_data = form_data.cleaned_data

            # Create Person Object
            new_person_id = uuid.uuid4()  # This lets you refer the other items to the person object
            new_person_obj = Person(id=new_person_id,
                                    name_first=cleaned_data['name_first'],
                                    name_middle=cleaned_data['name_middle'],
                                    name_last=cleaned_data['name_last'],
                                    gender=cleaned_data['gender'],
                                    client=True,
                                    employee=False
                                    )
            new_person_obj.save()

            # Test if phone data is present
            if cleaned_data['phone']:
                logging.debug("cleaned_data['phone'] = " + str(cleaned_data['phone'] +
                               "about to create new_phone_obj and save"))
                new_phone_obj = Phone(owner=new_person_obj,
                                      phone_number=cleaned_data['phone'],
                                      fax=False)
                new_phone_obj.save()
                logging.debug('Saved new_phone_obj')

            if cleaned_data['email']:
                logging.debug("cleaned_data['phone') = " + str(cleaned_data['email']) +
                              "About to try to create and save email object")
                new_email_obj = Email(owner=new_person_obj,
                                      address=cleaned_data['email'])
                new_email_obj.save()
                logging.debug("Saved new_email_obj")
            return HttpResponse('Saved object successfully')

        # Form data not valid-> repopulate form
        else:
            form = case_manager.forms.CreateNewClient
            return render(request, template_name='case_manager/create-new-client.html',
                          context={'form': form})


class CreateCaseView(UserPassesTestMixin, CreateView):
    """
    This allows staff to create new cases
    """
    model = Case
    template_name = 'case_manager/case_create.html'
    fields = ['type_of_case', 'date_started', 'client', 'related_parties', 'description_of_case',
              'hourly', 'attorney_hourly_rate', 'assistant_hourly_rate' ]

    def test_func(self):
        return (self.request.user.is_staff == True and
                self.request.user.is_active == True and
                self.request.user.has_perm('case_manager.can_add_case')
                )



class UpdateCaseView(UserPassesTestMixin, UpdateView):
    """
    This allows staff to update case objects
    """
    model = Case
    template_name = 'case_manager/generic_update.html'
    fields = ['type_of_case', 'date_started', 'client', 'related_parties', 'description_of_case',
              'hourly', 'attorney_hourly_rate', 'assistant_hourly_rate' ]

    def get_context_data(self, **kwargs):
        context = super(UpdateCaseView, self).get_context_data(**kwargs)
        context['name_of_object'] = 'Case'  # This tells the template what it is that we're editing
        context['action_html'] = reverse('case_manager:case_update', kwargs={'pk': self.object.id})
        return context

    def test_func(self):
        return (self.request.user.is_staff == True and
                self.request.user.is_active == True and
                self.request.user.has_perm('case_manager.can_change_case')
                )


class CaseDetailView(UserPassesTestMixin, DetailView):
    model = Case
    context_object_name = 'case'
    template = 'case_manager/case_detail.html'

    def test_func(self):
        return self.request.user.is_staff == True and self.request.user.is_active == True


@user_passes_test(user_is_staff)
def ClientListView(Request):
    """
    This allows staff to view all clients.
    """
    logging.debug('Entered ClientListView in case_manager.views')

    # Initially, set client list to all persons with client marked as true
    client_list = Person.objects.filter(client=True)

    # Set initial context to be sent to template
    context = {'client_list': client_list,
               'client_filter': case_manager.forms.ClientFilter}

    if Request.method == 'POST':
        logging.debug('Request method is post. Filtering results.')
        post_data = case_manager.forms.ClientFilter(Request.POST)

        # If post data valid, filter results by name searched
        if post_data.is_valid():
            logging.debug('Post request valid. Setting filters')

            # Set filters
            first_name_filter = post_data.cleaned_data['first_name']
            last_name_filter = post_data.cleaned_data['last_name']

            # Apply filters
            if first_name_filter != '':
                logging.debug('First name filter detected. Filtering...')
                client_list = client_list.filter(name_first__icontains=first_name_filter)
            if last_name_filter !='':
                logging.debug('Last name filter detected. Filtering....')
                client_list = client_list.filter(name_last__icontains=last_name_filter)

            # Update context
            context['client_list'] = client_list
            return render(Request, 'case_manager/client_index.html', context)

        # TO DO: If post data not valid, return form
        else:
            context['client_filter'] = post_data
            return render(Request, 'case_manager/client_index.html', context)

    # No post data, return all clients
    else:
        return render(Request, 'case_manager/client_index.html', context)

# TO DO: Add Delete Views