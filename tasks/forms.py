from django import forms

from .models import PRIORITIES, STATUSES, Context

# Constants

ITEM_TYPE = (
    ('both', 'both'),
    ('task', 'task'),
    ('project', 'project')
)

ROLE = (
    ('any', 'any'),
    ('created_by', 'creator'),
    ('supervisor', 'supervisor'),
    ('assigned_to', 'currently assigned'),
)

# Contants
STATUSES.append(('any', 'any'))  # Add an any option so that you can get all statuses

# Classes


class TaskFilter(forms.Form):
    """
    This class is used to filter tasks by context and priority
    """
    def __init__(self, *args, **kwargs):
        """
        This allows the view to pass in values to the taskfilter
        """
        request_user = kwargs.pop('request_user')
        super(TaskFilter, self).__init__(*args, **kwargs)
        self.fields['context_filter'].queryset = Context.objects.filter(user=request_user)

    context_filter = forms.ModelChoiceField(
        label='Context',
        queryset=None      # Queryset modified in init above
    )
    status_filter = forms.ChoiceField(label='Status',
                                      choices=STATUSES)
    item_filter = forms.ChoiceField(label='Type',
                                    choices=ITEM_TYPE)
    role_filter = forms.ChoiceField(label='Role',
                                    choices=ROLE)