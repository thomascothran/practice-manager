from django.db import models
from django.core.urlresolvers import reverse
import uuid
from people_and_property.models import Person

# Create your models here.

class CaseType(models.Model):
    """
    This model stores information about what types of cases I take.
    e.g., DNA, Agreed Divorce, Agreed Custody, Wills, etc.
    """
    BILLING_TYPES = (
        ('hourly', 'hourly'),
        ('flat rate', 'flat rate'),
        ('contingency', 'contingency'),
        ('hourly-capped', 'hourly, but capped')
    )


    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.TextField(max_length=50)
    description = models.TextField(max_length=500)
    billing_type = models.CharField(help_text='What type of billing is used for this sort of case?',
                                    choices=BILLING_TYPES, max_length=20)
    default_attorney_hourly_rate = models.DecimalField(help_text='What is the default hourly attorney rate?',
                                                       decimal_places=2, max_digits=10, null=True, blank=True)
    default_assistant_hourly_rate = models.DecimalField(help_text='What is the default hourly assistant rate?',
                                                        decimal_places=2, max_digits=10, null=True, blank=True)
    default_flat_rate = models.DecimalField(help_text='If flat rate, what is the total fee?',
                                            decimal_places=2, max_digits=15, null=True, blank=True)
    hourly_cap = models.DecimalField(help_text='If billing hourly with a total cap, what is the cap?',
                                     decimal_places=2, max_digits=15, null=True, blank=True)

    def __str__(self):
        return self.name

    # TO DO: Add absolute url


class Case(models.Model):
    """
    This class represents a case. A client may have multiple cases
    """
    STATUS_OPTIONS = (
        ('open', 'open'),
        ('closed except payment', 'Closed case, payment pending'),
        ('closed', 'paid and closed'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    type_of_case = models.ForeignKey(CaseType, related_name='case_set')
    created = models.DateTimeField(auto_now_add=True, help_text='When was this case created in our system?',
                                   null=True)
    updated = models.DateTimeField(auto_now=True, help_text='When was this case updated in our system?', null=True)
    date_started = models.DateField(help_text='What date did this case commence?')
    date_ended = models.DateField(help_text='What date did the case close?',
                                  blank=True, null=True)
    status = models.CharField(help_text='What is the current status of this case?', default='open',
                              choices=STATUS_OPTIONS, max_length=50)
    client = models.ManyToManyField(Person, related_name='case_set', limit_choices_to={'client': True})
    related_parties = models.ManyToManyField(Person, related_name='related_parties_set',
                                             help_text='Who else is related to the case (e.g., beneficiaries)',
                                             blank=True)
    description_of_case = models.TextField(help_text='What is the description of this case?',
                                           max_length=500, null=True)
    hourly = models.NullBooleanField(help_text='Are you getting paid by the hour?')
    attorney_hourly_rate = models.DecimalField(help_text=('What is the attorney hourly rate? If not specified, ' +
                                                          'default for case type will be used'),
                                               null=True, decimal_places=2, max_digits=15, blank=True)
    assistant_hourly_rate = models.DecimalField(help_text=('What is the assistant hourly rate on this case? If not' +
                                                           'specified, default for case type will be used'),
                                                null=True, decimal_places=2, max_digits=15, blank=True)
    total_billed = models.DecimalField(help_text='What is the total billed for this case?',
                                       null=True, decimal_places=2, max_digits=20, default=0.00)
    total_billings_received = models.DecimalField(help_text='What is the total billings you have received?',
                                                  null=True, decimal_places=2, max_digits=20, default=0.00)


    def __str__(self):
        """
        Str will pull the str of the first client linked as a client under the
        client attribute and add it to the type of case
        """
        return (str(self.client.all()[0]) + '-' + str(self.type_of_case))

    def get_absolute_url(self):
        return reverse('case_manager:case-detail', kwargs={'pk': self.pk})
