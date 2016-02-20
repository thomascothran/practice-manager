from django.test import Client
from django.test import TestCase
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

import logging

from ..models import Task, Project, Context

# LOGGING SETTINGS


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

    def test_that_inactive_users_are_redirected(self):
        """
        This tests to see if users whose 'is_active' attribute is set to false
        don't have access to the IndexVew
        """
        # Create inactive user
        inactive_user = User.objects.create_user(
            username='inactive_user',
            password='sdkflaj29342j',
            email='inactive_user@gmail.com',
            is_active=False
        )

        # Log inactive user in
        c = Client()
        c.force_login(inactive_user)

        # Try to load index view
        response = c.get(reverse('task_manager:index'), follow=True)

        # Test to see if user was redirected
        expected_url = '/accounts/login/?next=%s' % reverse('task_manager:index')
        self.assertRedirects(response, expected_url=expected_url)

    def test_filter_that_a_users_context_shows_up_in_filter(self):
        """
        This test ensures that a user's contexts shows up in the filter
        on the side of the page
        """
        test_superuser = User.objects.create_superuser(
            username='test_superuser_40291',
            email='test_superuser_40291',
            password='sdjfOIJ@42'
        )
        test_context = Context.objects.create(
            name='psdjew@#11',
            user=test_superuser
        )

        c = Client()
        c.force_login(test_superuser)
        response = c.get(reverse('task_manager:index'), follow=True)
        self.assertContains(response=response, text=str(test_context))


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
        redirect_url = '/accounts/login/?next=%s' % reverse('task_manager:task_detail', kwargs={'pk': test_task.id})
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
        expected_redirect_url = str('%s?next=%s' % (str(reverse('django_auth:login')), test_task.get_absolute_url()))
        self.assertRedirects( response, expected_redirect_url)

    def test_that_authorized_users_can_view_tasks(self):
        """
        This tests whether authorized users can view tasks.
        """
        # Create super user
        superuser_user = User.objects.create_superuser(
            username='test_superuser492kd',
            password='fdjfslkej0213@',
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
            response = c.get(reverse('task_manager:task_detail', kwargs={'pk': test_task.id}), follow=True)
            # Assert 200 response (success)
            self.assertEqual(
                200,
                response.status_code,
                msg='Authorized User %s redirected. Response: %s' % (authorized_user, response)
            )

    def test_that_inactive_users_are_redirected(self):
        """
        This tests to see if users whose 'is_active' attribute is set to false
        don't have access to task details
        """
        # Create inactive user
        inactive_user = User.objects.create_user(
            username='inactive_user',
            password='sdkflaj29342j',
            email='inactive_user@gmail.com',
            is_active=False
        )
        # Create superuser (creator for tasks)
        test_superuser = User.objects.create_superuser(
            username='test_superuser',
            password='alsfkj32o',
            email='test_superuser@gmail.com'
        )
        # Create task
        test_task = Task.objects.create(
            name='SDKfjwraa09 asd0fai093iasdfj a',
            created_by=test_superuser,
            supervisor=inactive_user,               # inactive_user is listed as the superuser, so
            status='pending',                       # but for inactive status, should have authorization
        )

        # Log inactive user in
        c = Client()
        c.force_login(inactive_user)

        # Try to load index view
        response = c.get(
                reverse('task_manager:task_detail',
                        kwargs={'pk': test_task.id}),
                follow=True
        )

        # Test to see if user was redirected
        expected_url = ('/accounts/login/?next=%s' %
                        reverse('task_manager:task_detail', kwargs={'pk': test_task.id}))
        self.assertRedirects(response, expected_url=expected_url)


class TaskCreateViewTest(TestCase):
    """
    This class tests the TaskCreate view.
    """
    def test_that_task_creation_page_is_up(self):
        """
        This tests that the task creation page returns a 200
        http message. Because in the future, task creation may be
        limited, we use a superuser.
        """
        test_superuser = User.objects.create_superuser(
            username='test_sup',
            password='kalsdjfq231',
            email='test_sup@gmail.com'
        )

        c = Client()
        c.force_login(test_superuser)
        response = c.get(reverse('task_manager:add_task'))
        self.assertEqual(200,
                         response.status_code,
                         msg=('When superuser tries to login to the task creation page, the server '+
                              'does not return a 200 code. This indicates there is something wrong ' +
                              'with the task creation view.')
                         )

    def test_that_anonymous_users_are_redirected_to_login_page(self):
        """
        This tests whether users who aren't logged in are forced to login
        when they try to create a task.
        """
        c = Client()
        response = c.get(reverse('task_manager:add_task'), follow=True)
        redirect_url = '/accounts/login/?next=%s' % reverse('task_manager:add_task')
        self.assertRedirects(response, redirect_url)

    def test_that_inactive_users_are_redirected(self):
        """
        This tests to see if users whose 'is_active' attribute is set to false
        don't have access to task creation view
        """
        # Create inactive user
        inactive_user = User.objects.create_user(
            username='inactive_user',
            password='sdkflaj29342j',
            email='inactive_user@gmail.com',
            is_active=False
        )

        # Log inactive user in
        c = Client()
        c.force_login(inactive_user)

        # Try to load index view
        response = c.get(reverse('task_manager:add_task'), follow=True)

        # Test to see if user was redirected
        expected_url = ('/accounts/login/?next=%s' % reverse('task_manager:add_task'))
        self.assertRedirects(response, expected_url=expected_url)

    def test_that_a_users_context_shows_up_in_task_creation_view(self):
        """
        This tests that the task creation page shows all contexts related
        to the user
        """
        test_superuser = User.objects.create_superuser(
            username='test_sup',
            password='kalsdjfq231',
            email='test_sup@gmail.com'
        )
        test_context = Context.objects.create(
            name='Hejw)wJ!',
            user=test_superuser
        )

        c = Client()
        c.force_login(test_superuser)
        response = c.get(reverse('task_manager:add_task'))
        self.assertContains(response=response, text='Hejw)wJ!')

    # TO DO def test_that_other_users_contexts_dont_show_up_in_task_creation_view(self):

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
        self.assertRedirects(response, expected_url=login_url)

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
        response = c.get(reverse('task_manager:task_update', kwargs={'pk': test_task.id}), follow=True)
        expected_url = '/accounts/login/?next=%s' % reverse('task_manager:task_update', kwargs={'pk': test_task.id})
        self.assertRedirects(
                response,
                expected_url=expected_url,
                msg_prefix='Unauthorized users have access to the task update page.'
        )

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
            username='test_superuser',
            password='asdkjf234fj',
            email='sldkfjeowo0@gmail.com'
        )

        staff_user = User.objects.create_user(
            username='test_staff_user',
            email='ghghos90@hotmail.com',
            is_staff=True,
        )

        # Create creator user (to be the creator of the task)
        creator_user = User.objects.create_user(
            username='test_creator_user',
            password='loggedinSUS12391',
            email = 'jimbo@hotmail.com'
        )

        # Create supervisor user
        supervisor_user = User.objects.create(
            username='test_supervisoruser',
            email='j2onjon@gmail.com'
        )

        # Create assigned user

        assigned_user = User.objects.create(
            username='test_assigneduser',
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
            response = c.get(reverse('task_manager:task_update', kwargs={'pk': test_task.id}), follow=True)
            # Assert 200 http code (success)
            self.assertEqual(
                200,
                response.status_code,
                msg='User %s does not get a 200 http code for request %s' % (authorized_user, response)
            )

    def test_that_inactive_users_are_redirected(self):
        """
        This tests to see if users whose 'is_active' attribute is set to false
        don't have access to task update view
        """
        # Create inactive user
        inactive_user = User.objects.create_user(
            username='inactive_user',
            password='sdkflaj29342j',
            email='inactive_user@gmail.com',
            is_active=False
        )
        # Create superuser (creator for tasks)
        test_superuser = User.objects.create_superuser(
            username='test_superuser',
            password='alsfkj32o',
            email='test_superuser@gmail.com'
        )
        # Create task
        test_task = Task.objects.create(
            name='SDKfjwraa09 asd0fai093iasdfj a',
            created_by=test_superuser,
            supervisor=inactive_user,               # inactive_user is listed as the superuser, so
            status='pending',                       # but for inactive status, should have authorization
        )

        # Log inactive user in
        c = Client()
        c.force_login(inactive_user)

        # Try to load index view
        response = c.get(
                reverse('task_manager:task_update',
                        kwargs={'pk': test_task.id}),
                follow=True
        )

        # Test to see if user was redirected
        expected_url = ('/accounts/login/?next=%s' %
                        reverse('task_manager:task_update', kwargs={'pk': test_task.id}))
        self.assertRedirects(response, expected_url=expected_url)


class ProjectDetailViewTest(TestCase):
    """
    This class tests the Project Detail View
    """
    def test_that_anonymous_users_are_redirected_to_login(self):
        # Create superuser (so that we can create project)
        test_superuser = User.objects.create_user(
            username='logged_in_super_user',
            password='loggedinSUS12391',
            email = 'jimbo@hotmail.com'
        )

        # Create project
        test_project = Project.objects.create(
            name='SDKfjwraa09 asd0fai093iasdfj a',
            created_by=test_superuser,
            supervisor=test_superuser,
            status='pending',
        )

        # See if anonymous client gets redirected to login page
        c = Client()
        response = c.get(reverse('task_manager:project_detail', kwargs={'pk':test_project.id}))
        login_url = '/accounts/login/?next=%s' % reverse('task_manager:project_detail', kwargs={'pk': test_project.id})
        self.assertRedirects(response, expected_url=login_url)

    def test_that_unauthorized_users_cant_open_project_detail_view(self):
        # Create superuser (so that we can create project)
        test_superuser = User.objects.create_user(
            username='logged_in_super_user',
            password='loggedinSUS12391',
            email = 'jimbo@hotmail.com'
        )

        # Create project
        test_project = Project.objects.create(
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
        response = c.get(reverse('task_manager:project_detail', kwargs={'pk': test_project.id}))
        expected_url = ('/accounts/login/?next=%s' %
                        reverse('task_manager:project_detail', kwargs={'pk': test_project.id}))
        self.assertRedirects(response, expected_url=expected_url)

    def test_that_authorized_users_can_get_to_project_detail_view(self):

        # Create super user
        superuser_user = User.objects.create_superuser(
            username='test_superuser492kd',
            password='asdkjf234fj',
            email='sldkfjeowo0@gmail.com'
        )

        # Create staff user
        staff_user = User.objects.create_user(
            username='test_staff_user',
            email='ghghos90@hotmail.com',
            is_staff=True,
        )

        # Create creator user (to be the creator of the project)
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

        # Create project
        test_project = Project.objects.create(
            name='SDKfjwraa09 asd0fai093iasdfj a',
            created_by=creator_user,
            supervisor=supervisor_user,
            status='pending',
        )

        # Add assigned user to project
        test_project.assigned_to.add(assigned_user)

        # Create list of authorizes users
        authorized_users = [assigned_user, creator_user, supervisor_user, superuser_user, staff_user]

        # Create client object
        c = Client()

        # Loop through authorized users to ensure they
        # get a 200 http code
        for authorized_user in authorized_users:
            c.force_login(authorized_user)
            # Request task update page
            response = c.get(reverse('task_manager:project_detail', kwargs={'pk': test_project.id}), follow=True)
            # Assert 200 response (success)
            self.assertEqual(200, response.status_code)

    def test_that_inactive_users_are_redirected(self):
        """
        This tests to see if users whose 'is_active' attribute is set to false
        don't have access to project detail view
        """
        # Create inactive user
        inactive_user = User.objects.create_user(
            username='inactive_user',
            password='sdkflaj29342j',
            email='inactive_user@gmail.com',
            is_active=False
        )
        # Create superuser (creator for project)
        test_superuser = User.objects.create_superuser(
            username='test_superuser',
            password='alsfkj32o',
            email='test_superuser@gmail.com'
        )
        # Create project
        test_project = Project.objects.create(
            name='SDKfjwraa09 asd0fai093iasdfj a',
            created_by=test_superuser,
            supervisor=inactive_user,               # inactive_user is listed as the superuser, so
            status='pending',                       # but for inactive status, should have authorization
        )

        # Log inactive user in
        c = Client()
        c.force_login(inactive_user)

        # Try to load index view
        response = c.get(
                reverse('task_manager:project_detail',
                        kwargs={'pk': test_project.id}),
                follow=True
        )

        # Test to see if user was redirected
        expected_url = ('/accounts/login/?next=%s' %
                        reverse('task_manager:project_detail', kwargs={'pk': test_project.id}))
        self.assertRedirects(response, expected_url=expected_url)


class ProjectCreateViewTest(TestCase):
    """
    This class test the ProjectCreate View
    """
    def test_that_project_creation_page_is_up(self):
        """
        This tests that the project creation page returns a 200
        http message. Because in the future, task creation may be
        limited to certain users, we use a superuser.
        """
        test_superuser = User.objects.create_superuser(
            username='test_sup',
            password='kalsdjfq231',
            email='test_sup@gmail.com'
        )

        c = Client()
        c.force_login(test_superuser)
        response = c.get(reverse('task_manager:add_project'), follow=True)
        self.assertEqual(200,
                         response.status_code,
                         msg=('When superuser tries to login to the task creation page, the server '+
                              'does not return a 200 code. The user is redirected to %s.' %
                              response.redirect_chain)
                         )

    def test_that_anonymous_users_are_redirected_to_login_page(self):
        """
        This tests whether users who aren't logged in are forced to login
        when they try to create a project.
        """
        c = Client()
        response = c.get(reverse('task_manager:add_project'), follow=True)
        redirect_url = '/accounts/login/?next=%s' % reverse('task_manager:add_project')
        self.assertRedirects(response, redirect_url)

    def test_that_inactive_users_are_redirected(self):
        """
        This tests to see if users whose 'is_active' attribute is set to false
        don't have access to task creation view
        """
        # Create inactive user
        inactive_user = User.objects.create_user(
            username='inactive_user',
            password='sdkflaj29342j',
            email='inactive_user@gmail.com',
            is_active=False
        )

        # Log inactive user in
        c = Client()
        c.force_login(inactive_user)

        # Try to load add project view
        response = c.get(reverse('task_manager:add_project'), follow=True)

        # Test to see if user was redirected
        expected_url = ('/accounts/login/?next=%s' % reverse('task_manager:add_project'))
        self.assertRedirects(response, expected_url=expected_url)


class ProjectUpdateViewTest(TestCase):
    """
    This class tests the Project Update view
    """

    def test_that_anonymous_users_are_redirected_to_login(self):
        # Create superuser (so that we can create project)
        test_superuser = User.objects.create_user(
            username='logged_in_super_user',
            password='loggedinSUS12391',
            email = 'jimbo@hotmail.com'
        )

        # Create project
        test_project = Project.objects.create(
            name='SDKfjwraa09 asd0fai093iasdfj a',
            created_by=test_superuser,
            supervisor=test_superuser,
            status='pending',
        )

        # See if anonymous client gets a 302 redirection
        c = Client()
        response = c.get(reverse('task_manager:update-project', kwargs={'pk':test_project.id}))
        login_url = '/accounts/login/?next=%s' % reverse('task_manager:update-project', kwargs={'pk': test_project.id})
        self.assertRedirects(response, expected_url=login_url)

    def test_that_unauthorized_users_cant_open_project_update_view(self):
        # Create superuser (so that we can create project)
        test_superuser = User.objects.create_user(
            username='logged_in_super_user',
            password='loggedinSUS12391',
            email = 'jimbo@hotmail.com'
        )

        # Create project
        test_project = Project.objects.create(
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

        # Request Project Update page
        response = c.get(reverse('task_manager:update-project', kwargs={'pk': test_project.id}))
        expected_url = '/accounts/login/?next=%s' % reverse('task_manager:update-project',
                                                            kwargs={'pk': test_project.id})
        self.assertRedirects(response, expected_url=expected_url)

    def test_that_viewers_of_projects_cant_edit_project(self):
        # Create superuser (so that we can create project)
        test_superuser = User.objects.create_user(
            username='logged_in_super_user',
            password='loggedinSUS12391',
            email = 'jimbo@hotmail.com'
        )

        # Create project
        test_project = Project.objects.create(
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

        # Add unauthorized user as a viewer to the project
        test_project.viewers.add(unauthorized_user)

        # Create client, use unauthorized_user's account to login
        c = Client()
        c.force_login(unauthorized_user)

        # Request Project Update page
        response = c.get(reverse('task_manager:update-project', kwargs={'pk': test_project.id}))
        expected_url = '/accounts/login/?next=%s' % reverse('task_manager:update-project',
                                                            kwargs={'pk': test_project.id})
        self.assertRedirects(response, expected_url=expected_url)

    def test_that_authorized_users_can_get_to_project_update_view(self):

        # Create super user
        superuser_user = User.objects.create_superuser(
            username='test_superuser492kd',
            password='asdkjf234fj',
            email='sldkfjeowo0@gmail.com'
        )

        staff_user = User.objects.create_user(
            username='test_staff_user',
            email='ghghos90@hotmail.com',
            is_staff=True,
        )

        # Create creator user (to be the creator of the project)
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

        # Create project
        test_project = Project.objects.create(
            name='SDKfjwraa09 asd0fai093iasdfj a',
            created_by=creator_user,
            supervisor=supervisor_user,
            status='pending',
        )

        # Add assigned user to project
        test_project.assigned_to.add(assigned_user)

        # Create list of authorizes users
        authorized_users = [assigned_user, creator_user, supervisor_user, superuser_user, staff_user]

        # Create client object
        c = Client()

        # Loop through authorized users to ensure they
        # get a 200 http code
        for authorized_user in authorized_users:
            c.force_login(authorized_user)
            # Request project update page
            response = c.get(reverse('task_manager:update-project', kwargs={'pk': test_project.id}), follow=True)
            # Assert 200 response (success)
            self.assertEqual(
                200,
                response.status_code,
                msg='Authorized user %s redirected. Response: %s' % (authorized_user, response)
            )

    def test_that_inactive_users_are_redirected(self):
        """
        This tests to see if users whose 'is_active' attribute is set to false
        don't have access to project update view
        """
        # Create inactive user
        inactive_user = User.objects.create_user(
            username='inactive_user',
            password='sdkflaj29342j',
            email='inactive_user@gmail.com',
            is_active=False
        )
        # Create superuser (creator for project)
        test_superuser = User.objects.create_superuser(
            username='test_superuser',
            password='alsfkj32o',
            email='test_superuser@gmail.com'
        )
        # Create project
        test_project = Project.objects.create(
            name='SDKfjwraa09 asd0fai093iasdfj a',
            created_by=test_superuser,
            supervisor=inactive_user,               # inactive_user is listed as the superuser, so
            status='pending',                       # but for inactive status, should have authorization
        )

        # Log inactive user in
        c = Client()
        c.force_login(inactive_user)

        # Try to load update project view
        response = c.get(
                reverse('task_manager:update-project',
                        kwargs={'pk': test_project.id}),
                follow=True
        )

        # Test to see if user was redirected
        expected_url = ('/accounts/login/?next=%s' %
                        reverse('task_manager:update-project', kwargs={'pk': test_project.id}))
        self.assertRedirects(response, expected_url=expected_url)


class SettingsViewTest(TestCase):
    """
    This tests the settings view
    """
    def test_that_anonymous_users_are_redirected_to_login(self):

        # See if anonymous client gets a 302 redirection
        c = Client()
        response = c.get(reverse('task_manager:settings'))
        login_url = '/accounts/login/?next=%s' % reverse('task_manager:settings')
        self.assertRedirects(response, expected_url=login_url)

    def test_that_inactive_users_are_redirected(self):
        """
        This tests to see if users whose 'is_active' attribute is set to false
        don't have access to the settings view
        """
        # Create inactive user
        inactive_user = User.objects.create_user(
            username='inactive_user',
            password='sdkflaj29342j',
            email='inactive_user@gmail.com',
            is_active=False
        )

        # Log inactive user in
        c = Client()
        c.force_login(inactive_user)

        # Try to load settings view
        response = c.get(reverse('task_manager:settings'), follow=True)

        # Test to see if user was redirected
        expected_url = ('/accounts/login/?next=%s' %
                        reverse('task_manager:settings'))
        self.assertRedirects(response, expected_url=expected_url)


class ContextTagCreate(TestCase):
    """
    This class tests the view that creates the context tag
    """

    def test_that_anonymous_users_are_redirected_to_login(self):
        # See if anonymous client gets redirected
        c = Client()
        response = c.get(reverse('task_manager:context_add'))
        login_url = '/accounts/login/?next=%s' % reverse('task_manager:context_add')
        self.assertRedirects(response, expected_url=login_url)

    def test_that_inactive_users_are_redirected(self):
        """
        This tests to see if users whose 'is_active' attribute is set to false
        don't have access to the context creation view
        """
        # Create inactive user
        inactive_user = User.objects.create_user(
            username='inactive_user',
            password='sdkflaj29342j',
            email='inactive_user@gmail.com',
            is_active=False
        )

        # Log inactive user in
        c = Client()
        c.force_login(inactive_user)

        # Try to load the view
        response = c.get(reverse('task_manager:context_add'), follow=True)

        # Test to see if user was redirected
        expected_url = ('/accounts/login/?next=%s' %
                        reverse('task_manager:context_add'))
        self.assertRedirects(response, expected_url=expected_url)


class ContextTagDetail(TestCase):
    """
    This class tests the context tag detail page
    """
    def test_that_anonymous_users_are_redirected_to_login(self):
        # Create superuser (so that we can create context)
        test_superuser = User.objects.create_user(
            username='logged_in_super_user',
            password='loggedinSUS12391',
            email = 'jimbo@hotmail.com'
        )

        # Create context
        test_context = Context.objects.create(
            name='SDKfjwraa09 asd0fai093iasdfj a',
            user=test_superuser,
        )

        # See if anonymous client gets redirected
        c = Client()
        response = c.get(reverse('task_manager:context_detail', kwargs={'pk':test_context.id}))
        login_url = '/accounts/login/?next=%s' % reverse('task_manager:context_detail', kwargs={'pk': test_context.id})
        self.assertRedirects(response, expected_url=login_url)

    def test_that_unauthorized_users_cant_open_context_detail_view(self):
        # Create superuser (so that we can create context)
        test_superuser = User.objects.create_user(
            username='logged_in_super_user',
            password='loggedinSUS12391',
            email = 'jimbo@hotmail.com'
        )

        # Create context
        test_context = Context.objects.create(
            name='SDKfjwraa09 asd0fai093iasdfj a',
            user=test_superuser,
        )

        # Create unauthorized user
        unauthorized_user = User.objects.create(
            username='asdlfjeworjijww39',
            email='jonjon@gmail.com'
        )

        # Create client, use unauthorized_user's account to login
        c = Client()
        c.force_login(unauthorized_user)

        # Request Context detail page
        response = c.get(reverse('task_manager:context_detail', kwargs={'pk': test_context.id}))
        expected_url = '/accounts/login/?next=%s' % reverse('task_manager:context_detail',
                                                            kwargs={'pk': test_context.id})
        self.assertRedirects(response, expected_url=expected_url)

    def test_that_authorized_users_can_get_to_context_detail_view(self):

        # Create super user
        superuser_user = User.objects.create_superuser(
            username='test_superuser492kd',
            password='asdkjf234fj',
            email='sldkfjeowo0@gmail.com'
        )

        staff_user = User.objects.create_user(
            username='test_staff_user',
            email='ghghos90@hotmail.com',
            is_staff=True,
        )

        # Create creator user (to be the creator of the project)
        creator_user = User.objects.create_user(
            username='logged_in_creator_user',
            password='loggedinSUS12391',
            email = 'jimbo@hotmail.com'
        )

        # Create the context
        test_context = Context.objects.create(
            name='SDKfjwraa09 asd0fai093iasdfj a',
            user=creator_user,
        )

        # Create list of authorizes users
        authorized_users = [creator_user, superuser_user, staff_user]

        # Create client object
        c = Client()

        # Loop through authorized users to ensure they
        # get a 200 http code
        for authorized_user in authorized_users:
            c.force_login(authorized_user)
            # Request context detail page
            response = c.get(reverse('task_manager:context_detail', kwargs={'pk': test_context.id}), follow=True)
            # Assert 200 response (success)
            self.assertEqual(
                200,
                response.status_code,
                msg='Authorized user %s redirected. Response: %s' % (authorized_user, response)
            )

    def test_that_inactive_users_are_redirected(self):
        """
        This tests to see if users whose 'is_active' attribute is set to false
        don't have access to context detail view
        """
        # Create inactive user
        inactive_user = User.objects.create_user(
            username='inactive_user',
            password='sdkflaj29342j',
            email='inactive_user@gmail.com',
            is_active=False
        )

        # Create context
        test_context = Context.objects.create(
            name='SDKfjwraa09 asd0fai093iasdfj a',
            user=inactive_user,
        )

        # Log inactive user in
        c = Client()
        c.force_login(inactive_user)

        # Try to load context detail view
        response = c.get(
                reverse('task_manager:context_detail',
                        kwargs={'pk': test_context.id}),
                follow=True
        )

        # Test to see if user was redirected
        expected_url = ('/accounts/login/?next=%s' %
                        reverse('task_manager:context_detail', kwargs={'pk': test_context.id}))
        self.assertRedirects(response, expected_url=expected_url)