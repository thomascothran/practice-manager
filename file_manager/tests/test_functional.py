from django.test import Client, TestCase
from django.contrib.staticfiles.testing import LiveServerTestCase
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from selenium import webdriver

import unittest

# Constants
test_superuser_username = 'test_sup_aj3j*(Y'
test_superuser_email = 'test_sup_234@gmail.com'
test_superuser_password = 'sdlfkj3232()*HT^'


class SeleniumTests(TestCase, LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(5)

        # Create objects for testing
        User.objects.create_superuser(
            username=test_superuser_username,
            email=test_superuser_email,
            password=test_superuser_password
        )

    def tearDown(self):
        self.browser.quit()

    # Helper functions
    def log_user_in(self, user_object, password):
        """
        This is designed to be a helper function that logs the user in.
        :param user_object: this is the user
        :param password: this is a string representing the password
        :return:
        """
        # First, check to see whether username and password authenticate directly
        # using authenticate()
        user_auth = authenticate(username=user_object.username, password=password)
        self.assertTrue(
            # If user couldn't be authenticated, user_auth returns None
            user_auth is not None,
            msg=('User authentication failed in test_functional.log_user_in() when' +
                 'it was attempted to login user with authenticate()')
        )
        # Now check to make sure that the test would fail with bad credentials
        user_not_auth = authenticate(username='absdflkjewrw2', password='werjksler3#@')
        self.assertFalse(
            user_not_auth is not None,
            msg='For some reason, attempt to authenticate non-logged in user succeeded.'
        )
        # Try to pull up task index, make sure you get redirected
        self.browser.get(str(self.live_server_url) + reverse('file_manager:note_index'))
        self.assertTrue('login' in self.browser.current_url)
        self.browser.implicitly_wait(10)
        # Login
        self.browser.find_element_by_name('username').send_keys(user_object.username)
        self.browser.find_element_by_name('password').send_keys(password)
        self.browser.find_element_by_name('submit').click()
        self.browser.implicitly_wait(10)
        return user_object


    def test_the_file_manager_index_redirected_anon_users(self):
        self.browser.get(self.live_server_url + reverse('file_manager:note_index'))
        # Check whether the browser goes to the login page.
        self.assertTrue(
            'login' in self.browser.current_url,
            msg='Current url is %s' % self.browser.current_url,
        )

    def test_that_authorized_users_can_reach_note_index_page(self):
        # Pull authorized users from database by putting each in a
        # dict of the user object and the password
        local_test_superuser = {
            'user': User.objects.get(username=test_superuser_username),
            'password': test_superuser_password
        }

        authorized_users = [local_test_superuser]
        # Loop through authorized users, seeing if they can get to the task page
        for authorized_user in authorized_users:
            self.log_user_in(
                user_object=authorized_user['user'],
                password=authorized_user['password']
            )
            self.browser.get(self.live_server_url + reverse('file_manager:note_index'))
            # Assert that we have reached the note index page
            self.assertEqual(
                self.browser.current_url,
                str(self.live_server_url + reverse('file_manager:note_index')),
                msg='User %s could not reach note index page' % authorized_user['user']
            )

    def test_that_user_can_create_note_and_see_it_in_note_index(self):
        local_test_superuser = {
            'user': User.objects.get(username=test_superuser_username),
            'password': test_superuser_password
        }
        self.log_user_in(
            user_object=local_test_superuser['user'],
            password=local_test_superuser['password']
        )
        # Navigate to note index and click add note
        self.browser.get(self.live_server_url + reverse('file_manager:note_index'))
        self.assertEqual(
            self.browser.current_url,
            str(self.live_server_url + reverse('file_manager:note_index'))
        )
        self.browser.find_element_by_name('sidebar_add_note')
        # Check to make sure we got to the add note page
        self.assertEqual(
            self.browser.current_url,
            str(self.live_server_url, reverse('file_manager:note_create'))
        )

if __name__ == '__main__':
    unittest.main(warnings='ignore')