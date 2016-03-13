from django.test import Client, TestCase
from django.contrib.staticfiles.testing import LiveServerTestCase
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from selenium import webdriver

from ..models import Note

import unittest

# Constants
test_superuser_username = 'test_sup_aj3j*(Y'
test_superuser_email = 'test_sup_234@gmail.com'
test_superuser_password = 'sdlfkj3232()*HT^'

test_superuser2_username = 'test_sup_JEIW()@'
test_superuser2_email = 'test_supH@gmail.com'
test_superuser2_password = 'aewlr3()*#J(#'

test_sup2_note_title = 'This is a test note 2302jOI@U'
test_sup2_note_title = 'Test HWL@@9#$H@'


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

        local_test_superuser2 = User.objects.create_superuser(
            username=test_superuser2_username,
            email=test_superuser2_email,
            password=test_superuser2_password
        )

        Note.objects.create(
            # This is superuser2's note
            title=test_sup2_note_title,
            creator=local_test_superuser2
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
        self.browser.find_element_by_name('sidebar_add_note').click()
        # Check to make sure we got to the add note page
        self.assertEqual(
            self.browser.current_url,
            str(self.live_server_url + reverse('file_manager:note_create'))
        )
        # Now, create a note
        self.browser.find_element_by_name('title').send_keys('H#OJdj2)(*')
        self.browser.find_element_by_name('submit_button').click()
        # Check to ensure we're not stuck on the note creation page
        self.assertNotEqual(
            self.browser.current_url,
            str(self.live_server_url + reverse('file_manager:note_create')),
            msg='We\'re stuck on the note creation page. Perhaps note detail page is not working?'
        )
        # Now go to the note index page
        self.browser.get('file_manager:note_index')
        # Now, check to see if the note appears on the page
        note_index_table = self.browser.find_element_by_name('note_index_table')
        self.assertIn(member='H#OJdj2)(*', container=note_index_table)


    def test_that_user_sees_own_notes_but_not_others(self):
        # First, get objects
        local_test_owner = User.objects.get(username=test_superuser2_username)
        local_test_note = Note.objects.get(title=test_sup2_note_title)
        local_test_nonowner = User.objects.get(username=test_superuser_username)

        # Log nonowner in
        self.log_user_in(
            user_object=local_test_nonowner,
            password=test_superuser_password
        )

        # Navigate to index
        self.browser.get(self.live_server_url + reverse('file_manager:note_index'))
        # Check to make sure we're there
        self.assertEqual(
            self.browser.current_url,
            str(self.live_server_url + reverse('file_manager:note_index'))
        )
        # TO DO: Now, assert that nonowner does not see the other's note


if __name__ == '__main__':
    unittest.main(warnings='ignore')