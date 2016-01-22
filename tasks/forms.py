from django import forms

from .models import CONTEXTS, PRIORITIES, STATUSES

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

# Classes


class TaskFilter(forms.Form):
    """
    This class is used to filter tasks by context and priority
    """
    priority_filter = forms.ChoiceField(label='Priority',
                                        choices=PRIORITIES)
    status_filter = forms.ChoiceField(label='Status',
                                      choices=STATUSES)
    item_filter = forms.ChoiceField(label='Type',
                                    choices=ITEM_TYPE)
    role_filter = forms.ChoiceField(label='Role',
                                    choices=ROLE)