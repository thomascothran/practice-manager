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

    # TO DO: def test_whether_unauthorized_users_are_redirected(self):
