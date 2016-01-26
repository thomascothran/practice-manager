from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.urlresolvers import reverse

from ..models import Project, Task, Context


class ProjectTestCase(TestCase):
    """
    This tests the Project model using unit testing.
    """

    def testProjectStr(self):
        """
        This just tests that the __str__ return the name
        """
        # Create a user
        logged_in_superuser = User.objects.create_user(
            username='logged_in_super_user',
            password='loggedinSUS12391',
            email = 'jimbo@hotmail.com'
        )

        # Create a project
        test_project = Project.objects.create(
            name='This is a test project.',
            purpose='The purpose is to ensure that the Projects model is ok.',
            vision='Make surethis does not show up in testing.',
            created_by=logged_in_superuser,
            assigned_to=logged_in_superuser,
            supervisor=logged_in_superuser,
        )
        self.assertEqual(str(test_project), test_project.name)


    def testNestedProjects(self):
        """
        Test whether projects can be nested under each other using the
        project.under_project attribute.
        """
        # Create a user
        logged_in_superuser = User.objects.create_user(
            username='logged_in_super_user',
            password='loggedinSUS12391',
            email = 'jimbo@hotmail.com'
        )

        # Create test_project1

        Project.objects.create(
            name='This is a test project.',
            purpose='The purpose is to ensure that the Projects model is ok.',
            vision='Make surethis does not show up in testing.',
            created_by=logged_in_superuser,
            assigned_to=logged_in_superuser,
            supervisor=logged_in_superuser,
            level='1',
        )

        test_project1 = Project.objects.get(
            name='This is a test project.',
            level='1',
        )

        # Create test_project2
        Project.objects.create(
            name='This is another test project.',
            purpose='The purpose is to ensure that the Projects model is ok.',
            vision='Make sure this does not show up in testing.',
            created_by=logged_in_superuser,
            assigned_to=logged_in_superuser,
            supervisor=logged_in_superuser,
            level='2',
        )

        test_project2 = Project.objects.get(
            name='This is another test project.',
            vision='Make sure this does not show up in testing.',
        )

        # Make test_project1 and test_project2 related
        test_project2.under_projects.add(test_project1)

        # ASSERT RELATION BETWEEN PROJECTS

        self.assertEqual(                           # This asserts checks the attribute directly
                test_project1,
                test_project2.under_projects.get(
                        name=test_project1.name)
        )

        self.assertEqual(                           # This uses the reverse lookup to make sure the
                test_project2,                      # reverse relationship is set up correctly
                test_project1.subordinate_projects.get(name=test_project2.name)
        )


class TaskTestCase(TestCase):
    """
    This class tests the tasks models.
    """

    def testCreateTask(self):
        """
        This tests whether a task can be created.
        """

        # Create a user
        User.objects.create_user(
            username='logged_in_super_user',
            password='loggedinSUS12391',
            email = 'jimbo@hotmail.com'
        )

        logged_in_superuser = User.objects.get(username='logged_in_super_user')

        # Create a task
        Task.objects.create(
            name='SDKfjwraa09 asd0fai093iasdfj a',
            created_by=logged_in_superuser,
            assigned_to=logged_in_superuser,
            supervisor=logged_in_superuser,
            status='pending',
        )

        # Test that class is created
        assert Task.objects.get(name='SDKfjwraa09 asd0fai093iasdfj a')


    def testWhetherTaskRelatesToProject(self):
        """
        This tests whether a task can be related to a Project
        """

        # Create a user
        User.objects.create_user(
            username='logged_in_super_user',
            password='loggedinSUS12391',
            email = 'jimbo@hotmail.com'
        )

        logged_in_superuser = User.objects.get(username='logged_in_super_user')

        # Create a task
        Task.objects.create(
            name='SDKfjwraa09 asd0fai093iasdfj a',
            created_by=logged_in_superuser,
            assigned_to=logged_in_superuser,
            supervisor=logged_in_superuser,
            status='pending',
        )

        test_task = Task.objects.get(
            name='SDKfjwraa09 asd0fai093iasdfj a'
        )

        # Create a project

        Project.objects.create(
            name='This is a test project.',
            purpose='The purpose is to ensure that the Projects model is ok.',
            vision='Make surethis does not show up in testing.',
            created_by=logged_in_superuser,
            assigned_to=logged_in_superuser,
            supervisor=logged_in_superuser,
        )

        test_project = Project.objects.get(
            name='This is a test project.',
            purpose='The purpose is to ensure that the Projects model is ok.',
            vision='Make surethis does not show up in testing.',
        )

        test_task.related_projects.add(test_project)

        # Test whether test_project is accessible through
        # test_task.related_projects attribute
        self.assertEqual(test_project,
                         test_task.related_projects.get(name=test_project.name))

        # Test the reverse relationship. Is the task related to the project
        # through the project.task_set attribute
        self.assertEqual(test_task,
                         test_project.task_set.get(name=test_task.name))