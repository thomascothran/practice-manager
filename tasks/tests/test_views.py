from django.test import Client
from django.test import TestCase
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from ..models import Task

class IndexViewTests(TestCase):
    """
    This class tests the index view
    """

    def test_that_anonymous_users_are_redirected_to_login_page(self):
        """
        This tests to ensure that the page anonymous users are redirected
        to is the login page.
        """
        c = Client()
        response = c.get(reverse('task_manager:index'), follow=True)
        url_redirect = '/accounts/login/?next=%s' % reverse('task_manager:index')
        self.assertRedirects(response, url_redirect)

class TaskDetailView(TestCase):
    """
    This class tests the TaskDetail view
    """

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
            supervisor=test_superuser,
            status='pending',
        )

        c = Client()
        response = c.get(reverse('task_manager:task_detail', kwargs={'pk': test_task.id}), follow=True)
        redirect_url = 'accounts/login/?next=%s' % reverse('task_manager:task_detail', kwargs={'pk': test_task.id})
        self.assertRedirects(response, redirect_url)

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

    def test_that_authorized_users_can_view_tasks(self):
        """
        This tests whether authorized users can view tasks.
        """
        # Create super user
        superuser_user = User.objects.create_superuser(
            username='test_superuser492kd',
            email='sldkfjeowo0@gmail.com'
        )

        staff_user = User.objects.create_user(
            username='test_staff_user',
            email='ghghos90@hotmail.com',
            is_staff=True,
        )

        # Create creator user (to be the creator of the task)
        creator_user = User.objects.create_user(
            username='logged_in_creator_user',
            password='loggedinSUS12391',
            email = 'jimbo@hotmail.com'
        )

        # Create supervisor user
        supervisor_user = User.objects.create(
            username='asdll3232lfjeworjijww39',
            email='j2onjon@gmail.com'
        )

        # Create assigned user

        assigned_user = User.objects.create(
            username='asdlfjeasfjlworjijww39',
            email='jonj9on@gmail.com'
        )

        # Create task
        test_task = Task.objects.create(
            name='SDKfjwraa09 asd0fai093iasdfj a',
            created_by=creator_user,
            supervisor=supervisor_user,
            status='pending',
        )

        # Add assigned user to tasks
        test_task.assigned_to.add(assigned_user)

        # Create list of authorizes users
        authorized_users = [assigned_user, creator_user, supervisor_user, superuser_user, staff_user]

        # Create client object
        c = Client()

        # Loop through authorized users to ensure they
        # get a 200 http code
        for authorized_user in authorized_users:
            c.force_login(authorized_user)
            # Request task update page
            response = c.get(reverse('task_manager:task_detail', kwargs={'pk': test_task.id}))
            # Assert 200 response (success)
            self.assertEqual(200, response.status_code)

# class TaskCreateViewTest(TestCase):


class TaskUpdateViewTest(TestCase):
    """
    This tests the TaskUpdateVew.
    """
    def test_that_anonymous_users_are_redirected_to_login(self):
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
            supervisor=test_superuser,
            status='pending',
        )

        # See if anonymous client gets a 302 redirection
        c = Client()
        response = c.get(reverse('task_manager:task_update', kwargs={'pk':test_task.id}))
        login_url = '/accounts/login/?next=%s' % reverse('task_manager:task_update', kwargs={'pk': test_task.id})
        self.assertEqual(302, response.status_code)

    def test_that_unauthorized_users_cant_open_task_update_view(self):
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
            supervisor=test_superuser,
            status='pending',
        )

        # Create unauthorized user
        unauthorized_user = User.objects.create(
            username='asdlfjeworjijww39',
            email='jonjon@gmail.com'
        )

        # Create client, use unauthorized_user's account to login
        c = Client()
        c.force_login(unauthorized_user)

        # Request Task Update page
        response = c.get(reverse('task_manager:task_update', kwargs={'pk': test_task.id}))
        expected_url = '/accounts/login/?next=%s' % reverse('task_manager:task_update', kwargs={'pk': test_task.id})
        self.assertRedirects(response, expected_url=expected_url)

    def test_that_viewers_of_tasks_cant_edit_task(self):
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
            supervisor=test_superuser,
            status='pending',
        )

        # Create unauthorized user
        unauthorized_user = User.objects.create(
            username='asdlfjeworjijww39',
            email='jonjon@gmail.com'
        )

        # Add unauthorized user as a viewer to the task
        test_task.viewers.add(unauthorized_user)

        # Create client, use unauthorized_user's account to login
        c = Client()
        c.force_login(unauthorized_user)

        # Request Task Update page
        response = c.get(reverse('task_manager:task_update', kwargs={'pk': test_task.id}))
        expected_url = '/accounts/login/?next=%s' % reverse('task_manager:task_update', kwargs={'pk': test_task.id})
        self.assertRedirects(response, expected_url=expected_url)

    def test_that_authorized_users_can_get_to_task_update_view(self):

        # Create super user
        superuser_user = User.objects.create_superuser(
            username='test_superuser492kd',
            email='sldkfjeowo0@gmail.com'
        )

        staff_user = User.objects.create_user(
            username='test_staff_user',
            email='ghghos90@hotmail.com',
            is_staff=True,
        )

        # Create creator user (to be the creator of the task)
        creator_user = User.objects.create_user(
            username='logged_in_creator_user',
            password='loggedinSUS12391',
            email = 'jimbo@hotmail.com'
        )

        # Create supervisor user
        supervisor_user = User.objects.create(
            username='asdll3232lfjeworjijww39',
            email='j2onjon@gmail.com'
        )

        # Create assigned user

        assigned_user = User.objects.create(
            username='asdlfjeasfjlworjijww39',
            email='jonj9on@gmail.com'
        )

        # Create task
        test_task = Task.objects.create(
            name='SDKfjwraa09 asd0fai093iasdfj a',
            created_by=creator_user,
            supervisor=supervisor_user,
            status='pending',
        )

        # Add assigned user to tasks
        test_task.assigned_to.add(assigned_user)

        # Create list of authorizes users
        authorized_users = [assigned_user, creator_user, supervisor_user, superuser_user, staff_user]

        # Create client object
        c = Client()

        # Loop through authorized users to ensure they
        # get a 200 http code
        for authorized_user in authorized_users:
            c.force_login(authorized_user)
            # Request task update page
            response = c.get(reverse('task_manager:task_update', kwargs={'pk': test_task.id}))
            # Assert 200 response (success)
            self.assertEqual(200, response.status_code)
