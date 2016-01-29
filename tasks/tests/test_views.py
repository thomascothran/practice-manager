from django.test import Client
from django.test import TestCase
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from ..models import Task

class IndexViewTests(TestCase):
    """
    This class tests the index view
    """

    def test_that_anonymous_users_are_redirected_via_302_code(self):
        """
        This tests that users who are not logged in are redirected
        via a 302 code
        """

        c = Client()
        response = c.get(reverse('task_manager:index'))
        self.assertEqual(302, response.status_code)     # 302 is the response code for redirection.

    def test_that_anonymous_users_are_redirected_to_login_page(self):
        """
        This tests to ensure that the page anonymous users are redirected
        to is the login page.
        """
        c = Client()
        response = c.get(reverse('task_manager:index'), follow=True)
        self.assertTrue('login' in response.redirect_chain[0][0])

class TaskDetailView(TestCase):
    """
    This class tests the TaskDetail view
    """

    def test_that_anonymous_users_are_redirected_via_302_code(self):
        """
        This tests to see that anonymous users don't have access to
        any task details
        """

        # Create superuser (so that we can create task)
        test_superuser = User.objects.create_user(
            username='logged_in_super_user',
            password='loggedinSUS12391',
            email = 'jimbo@hotmail.com'
        )

        # Create task
        test_task = Task.objects.create(
            name='SDKfjwraa09 asd0fai093iasdfj a',
            created_by=test_superuser,
            assigned_to=test_superuser,
            supervisor=test_superuser,
            status='pending',
        )

        # See if anonymous client gets a 302 redirection
        c = Client()
        response = c.get(test_task.get_absolute_url())
        self.assertEqual(302, response.status_code)

    def test_that_anonymous_users_are_redirected_to_login_page(self):
        """
        This tests to ensure that the page anonymous users are redirected
        to is the login page.
        """
        # Create superuser (so that we can create task)
        test_superuser = User.objects.create_user(
            username='logged_in_super_user',
            password='loggedinSUS12391',
            email = 'jimbo@hotmail.com'
        )

        # Create task
        test_task = Task.objects.create(
            name='SDKfjwraa09 asd0fai093iasdfj a',
            created_by=test_superuser,
            assigned_to=test_superuser,
            supervisor=test_superuser,
            status='pending',
        )

        c = Client()
        response = c.get(test_task.get_absolute_url(), follow=True)
        self.assertTrue('login' in response.redirect_chain[0][0])

    def test_that_logged_in_users_cant_view_task_if_they_are_not_involved(self):
        """
        This tests whether one user can view another user's task if he/she is
        the creator, assignee, or
        """
        # Create a user so that you can create a task

        test_superuser = User.objects.create_user(
            username='logged_in_super_user',
            password='loggedinSUS12391',
            email = 'jimbo@hotmail.com'
        )

        # Create task
        test_task = Task.objects.create(
            name='SDKfjwraa09 asd0fai093iasdfj a',
            created_by=test_superuser,
            assigned_to=test_superuser,
            supervisor=test_superuser,
            status='pending',
        )

        # Create an unrelated user who shouldn't be able to see task
        test_unrelated_user = User.objects.create_user(
            username='afslkjo23ie',
            password='asdflkj234)(*',
            email='random@alksjdf.com'
        )

        c = Client()
        c.login(username=test_unrelated_user.username, password=test_unrelated_user.password)
        response = c.get(test_task.get_absolute_url(), follow=True)
        print(response.status_code)
        self.assertEqual(302, response.status_code)