from django.test import Client
from django.test import TestCase
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

import logging
from datetime import date

# Constants
test_superuser_username = 'test_su_flaks3'
test_superuser_password = 'aslk312ej#D@'
test_superuser_email = 'tec@gmail.com'

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
        self.assertTemplateUsed(response=response, template_name='file_manager/note_index.html')

    def test_that_authorized_users_can_see_note_index(self):
        # Make list of authorized users
        local_test_superuser = User.objects.get(username=test_superuser_username)
        authorized_users = [local_test_superuser]

        client = Client()
        for authorized_user in authorized_users:
            client.force_login(user=authorized_user)
            response = client.get(reverse('file_manager:note_index'))
            self.assertTrue(response.status_code is 200)

    def test_that_anonymous_users_cannot_see_note_index(self):
        client = Client()
        response = client.get(reverse('file_manager:note_index'), follow=True)
        url_redirect = '/accounts/login/?next=%s' % reverse('file_manager:note_index')
        self.assertRedirects(response=response, expected_url=url_redirect)

    # TO DO: def test_whether_unauthorized_users_are_redirected(self):
