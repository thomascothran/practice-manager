from django.test import Client
from django.test import TestCase
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

import logging
from datetime import date

from ..models import Note

# Constants
test_superuser_username = 'test_su_flaks3'
test_superuser_password = 'aslk312ej#D@'
test_superuser_email = 'tec@gmail.com'

test_note_title = 'test_note_324jsfO#IJ@4'


class NoteIndexViewTests(TestCase):

    def setUp(self):
        User.objects.create_superuser(
            username=test_superuser_username,
            email=test_superuser_email,
            password=test_superuser_password
        )

    def tearDown(self):
        pass

    def test_that_template_is_used(self):
        """
        This tests whether the proper index template is used
        """
        client = Client()
        test_superuser = User.objects.get(username=test_superuser_username)
        client.force_login(user=test_superuser)
        response = client.get(reverse('file_manager:note_index'), follow=True)
        self.assertTemplateUsed(
            response=response,
            template_name='file_manager/note_index.html'
        )

    def test_that_authorized_users_can_see_note_index(self):
        # Make list of authorized users
        local_test_superuser = User.objects.get(
            username=test_superuser_username
        )
        authorized_users = [local_test_superuser]

        client = Client()
        for authorized_user in authorized_users:
            client.force_login(user=authorized_user)
            response = client.get(reverse('file_manager:note_index'))
            self.assertTrue(response.status_code is 200)

    def test_that_anonymous_users_cannot_see_note_index(self):
        client = Client()
        response = client.get(reverse('file_manager:note_index'), follow=True)
        url_redirect = ('/accounts/login/?next=%s' %
                        reverse('file_manager:note_index'))
        self.assertRedirects(response=response, expected_url=url_redirect)


class NoteCreateView(TestCase):
    """
    This class tests the note create view
    """
    def setUp(self):
        User.objects.create_superuser(
            username=test_superuser_username,
            email=test_superuser_email,
            password=test_superuser_password
        )

    def tearDown(self):
        pass

    def test_whether_note_create_view_uses_correct_template(self):
        client = Client()
        test_superuser = User.objects.get(username=test_superuser_username)
        client.force_login(test_superuser)
        response = client.get(reverse('file_manager:note_create'), follow=True)
        self.assertTemplateUsed(
            response=response,
            template_name='file_manager/note_create.html'
        )

    def tests_whether_anonymous_users_are_redirected(self):
        client = Client()
        response = client.get(reverse('file_manager:note_create'))
        expected_url = ('/accounts/login/?next=%s' %
                        reverse('file_manager:note_create'))
        self.assertRedirects(
            response=response,
            expected_url=expected_url
        )

    def tests_whether_authorized_users_have_access_to_note_creation_view(self):
        client = Client()
        # Make a list of authorized users
        local_test_superuser = User.objects.get(
            username=test_superuser_username
        )
        authorized_users = [local_test_superuser]
        # See if authorized users have access
        for authorized_user in authorized_users:
            client.force_login(authorized_user)
            response = client.get(reverse('file_manager:note_create'))
            self.assertEqual(200, response.status_code)


class NoteDetailsViewTest(TestCase):
    """
    This class of tests tests the note details view
    """

    def setUp(self):
        local_user = User.objects.create_superuser(
            username=test_superuser_username,
            email=test_superuser_email,
            password=test_superuser_password
        )

        Note.objects.create(
            title=test_note_title,
            creator=local_user
        )

    def tearDown(self):
        pass

    def test_whether_task_details_uses_correct_template(self):
        client = Client()
        # Pull objects from db
        local_test_superuser = User.objects.get(
            username=test_superuser_username
        )
        local_test_note = Note.objects.get(title=test_note_title)
        client.force_login(local_test_superuser)
        response = client.get(
            reverse(
                'file_manager:note_details',
                kwargs={'pk': local_test_note.id})
        )
        self.assertTemplateUsed(
            response,
            template_name='templates/file_manager/note_detail.html'
        )

    def test_that_anon_users_are_redirected_from_note_detail_view(self):
        client = Client()
        # Pull note obj from db
        local_test_note = Note.objects.get(title=test_note_title)
        response = client.get(
            reverse(
                'file_manager:note_details',
                kwargs={'pk': local_test_note.id })
        )
        expected_url = ('/accounts/login/?next=%s' %
                        reverse('file_manager:note_details'))
        self.assertRedirects(
            response=response,
            expected_url=expected_url
        )
