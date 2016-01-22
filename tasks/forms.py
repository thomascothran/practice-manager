from django import forms

from .models import PRIORITIES, STATUSES
from .utils import get_users_contexts

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
    def __init__(self, user, *args, **kwargs):
        """
        This allows the view to pass in values to the taskfilter
        :param user: This is the request.user
        """
        super(TaskFilter, self).__init__(*args, **kwargs)
        self.fields['context_filter'].queryset = get_users_contexts(user)

    priority_filter = forms.ChoiceField(label='Priority',
                                        choices=PRIORITIES)
    context_filter = forms.ModelMultipleChoiceField(label='Context',
                                                    queryset=None)      # Queryset modified in init above
    status_filter = forms.ChoiceField(label='Status',
                                      choices=STATUSES)
    item_filter = forms.ChoiceField(label='Type',
                                    choices=ITEM_TYPE)
    role_filter = forms.ChoiceField(label='Role',
                                    choices=ROLE)