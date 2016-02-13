from selenium import webdriver
from selenium.webdriver.support.ui import Select
import unittest

from django.core.urlresolvers import reverse
from django.test import TestCase, RequestFactory
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth.models import User

# Constants
test_superuser_username = 'test_superuser_998'          # Setting up username and password strings
test_superuser_email = 'test_superuser_998@gmail.com'   # here so that they can be referenced below
test_superuser_password = 'slafj3430WIER93@#'
test_user_username = 'test_user_998'
test_user_password = 'ska;fljewerwfjsl#@2'
test_user_email = 'testuser98@gmail.com'


class BasicTest(StaticLiveServerTestCase):
    """
    This class just checks to make sure that the basics of the task
    manager are up and working.
    """

    # Setup and teardown
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(4)

    def tearDown(self):
        self.browser.quit()

    def create_user(self, superuser=True):
        """
        This is a helper function to create and return a user. Don't change
        usernames or passwords--it will break the functionality of the tests
        """
        if superuser == True:
            test_superuser = User.objects.create_superuser(
                username=test_superuser_username,
                email=test_superuser_email,
                password=test_superuser_password,
            )
            return test_superuser
        else:
            test_user = User.objects.create_user(
                username=test_user_username,
                email=test_user_email,
                password=test_user_password
            )
            return test_user

    def log_user_in(self, user_object, password):
        """
        This is designed to be a helper function that logs the user in.
        :param user_object: this is the user
        :param password: this is a string representing the password
        :return:
        """
        # Try to pull up task index, make sure you get redirected
        self.browser.get(str(self.live_server_url) + reverse('task_manager:index'))
        self.assertTrue('login' in self.browser.current_url)
        # Login
        self.browser.find_element_by_name('username').send_keys(user_object.username)
        self.browser.find_element_by_name('password').send_keys(password)
        self.browser.find_element_by_name('submit').click()
        self.browser.implicitly_wait(10)


    def test_create_task_and_check_that_it_shows_up_in_the_task_manager_index(self):
        # Create user
        self.user = self.create_user(superuser=True)
        # Log the user in
        self.log_user_in(user_object=self.user, password=test_superuser_password)
        self.browser.implicitly_wait(10)
        # Pull up the main task manager page
        self.browser.get(str(self.live_server_url) + reverse('task_manager:index'))
        # Make sure we go to the task manager index
        task_index_url = str(self.live_server_url) + reverse('task_manager:index')
        self.browser.get(task_index_url)
        self.assertTrue(str(task_index_url) == self.browser.current_url,
                        msg=('Assertion that current_url is %s failed. Current_url is %s' %
                             (str(reverse('task_manager:index')), self.browser.current_url)))
        # Click the 'add task' button on the sidebar
        add_task_taskbar_button = self.browser.find_element_by_name('add_task_sidebar_link')
        add_task_taskbar_button.click()
        self.browser.implicitly_wait(4)
        # Assert that it takes us to the add task page
        self.assertTrue(str(reverse('task_manager:add_task')) in self.browser.current_url)
        # Fill out form
        name_input = self.browser.find_element_by_name('name')
        name_input.send_keys('Test Name BfC02@@')
        assigned_to_dropdown = Select(self.browser.find_element_by_name('assigned_to'))
        assigned_to_dropdown.select_by_visible_text(str(self.user))
        supervisor_dropdown = Select(self.browser.find_element_by_name('supervisor'))
        supervisor_dropdown.select_by_visible_text(str(self.user))
        name_input.submit()
        self.browser.implicitly_wait(4)
        # Go to the index page, make sure test task shows up
        self.browser.get(str(self.live_server_url) + reverse('task_manager:index'))
        self.browser.implicitly_wait(4)
        # Check to ensure you are on the index page
        self.assertEqual(self.browser.current_url, str(self.live_server_url + reverse('task_manager:index')))
        # See if the task is in the table
        task_table = self.browser.find_element_by_name('task_table')
        task_table_rows = task_table.find_elements_by_tag_name('tr')
        self.assertTrue(
            any('Test Name BfC02@@' in row.text for row in task_table_rows),
            msg='The task is not showing up in the task index table'
        )


        # How to select options: https://stackoverflow.com/questions/24498976/python-selenium-select-from-drop-down-menu




if __name__ == '__main__':
    unittest.main(warnings='ignore')

