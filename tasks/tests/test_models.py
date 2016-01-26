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
