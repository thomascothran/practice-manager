from django.test import TestCase
from django.contrib.auth.models import User

from ..forms import TaskFilter
from ..models import Context

import unittest

# CONSTANTS
test_supervisor_username = 'test_superuser_jP2'
test_supervisor_password = 't2est_supe@ruser_jP3'
test_supervisor_email = 'test_superuser_jP2@gmail.com'
test_context_name = 'Test Context Nenwo!#$'

# TESTS
class TaskFilterTestCase(TestCase):
    """
    This class tests the task filter, which can be found
    in forms.
    """
    def setUp(self):
        # Create a user and a context
        test_supervisor = User.objects.create_superuser(
            username=test_supervisor_username,
            password=test_supervisor_password,
            email=test_supervisor_email

        )
        test_context = Context.objects.create(
            name=test_context_name,
            user=test_supervisor
        )
    def test_that_task_filter_takes_validates_data(self):
        # Pull context from database so we can get its id
        test_context = Context.objects.get(name=test_context_name)
        # Pull supervisor from db so we can instantiate the form
        test_supervisor = User.objects.get(username=test_supervisor_username)
        # Build dictionary that represents entering data in TaskFilter
        form_data = {
            'status_filter': 'pending',
            'item_filter': 'both',
            'role_filter': 'any',
            'context_filter': str(test_context.id)
        }
        # Bind data to TaskFilter, assert that it is valid
        task_filter = TaskFilter(data=form_data, request_user=test_supervisor)
        self.assertTrue(
            task_filter.is_valid(),
            msg=('Attempt to send data to TaskFilter is not validating. Error is: %s' %
                 task_filter.errors)
        )

    def test_that_task_filter_returns_context_after_validations(self):
        #  # Pull context from database so we can get its id
        test_context = Context.objects.get(name=test_context_name)
        # Pull supervisor from db so we can instantiate the form
        test_supervisor = User.objects.get(username=test_supervisor_username)
        # Build dictionary that represents entering data in TaskFilter
        form_data = {
            'status_filter': 'pending',
            'item_filter': 'both',
            'role_filter': 'any',
            'context_filter': str(test_context.id)
        }
        task_filter = TaskFilter(data=form_data, request_user=test_supervisor)
        # Run the is.valid() method so that we can access the cleaned_data
        task_filter.is_valid()
        cleaned_data = task_filter.cleaned_data
        self.assertEqual(
            cleaned_data['context_filter'],
            test_context,
            msg=(('The context filter entry in task_filter is not equal to the test context.' +
                  'context_filter is %s' % task_filter['context_filter']))
        )


if __name__ == '__main__':
    unittest.main(warnings='ignore')
