from django.test import Client
from django.test import TestCase
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from ..models import Task, Project, Context
from ..utils import apply_filters_from_task_filter

class ApplyFiltersFromTaskFilterTest(TestCase):
    """
    This class tests the apply_filters_from_task_filter
    helper function.
    """

    def test_whether_helper_function_filters_tasks_by_context(self):
        # Create a user and a context
        test_supervisor = User.objects.create_superuser(
            username='test_supervisor_ukKk03',
            password='testafaq3djOK',
            email='test_supervisor_ukKk03'

        )
        test_context = Context.objects.create(
            name='test_context_SDF3pwe21@',
            user=test_supervisor
        )
        test_task = Task.objects.create(
            name='test_task_345sdf230',
            created_by=test_supervisor,
            supervisor=test_supervisor,
        )
        # Add test_context to test_task
        test_task.context.add(test_context)

        # Build Dict to be submitted to the form
        form_data = {
            'status_filter': 'pending',
            'item_filter': 'both',
            'role_filter': 'any',
            'context_filter': str(test_context.id)
        }

        # Now call apply_filters_from_task_filter helper function
        (resulting_tasks, resulting_projects) = apply_filters_from_task_filter(
                requesting_user=test_supervisor,
                post_dict=form_data
        )
        self.assertTrue(
            test_task in list(resulting_tasks),
            msg=('apply_filters_from_task_filter is not filtering by context. resulting_tasks is %s' %
                 list(resulting_tasks))
        )