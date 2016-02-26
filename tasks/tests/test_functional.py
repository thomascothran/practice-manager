from selenium import webdriver
from selenium.webdriver.support.ui import Select
import unittest

from django.core.urlresolvers import reverse
from django.test import TestCase, RequestFactory
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth.models import User

from ..models import Context, Task, Project

# Constants
test_superuser_username = 'test_superuser_998'          # Setting up username and password strings
test_superuser_email = 'test_superuser_998@gmail.com'   # here so that they can be referenced below
test_superuser_password = 'slafj3430WIER93@#'
test_user_username = 'test_user_998'
test_user_password = 'ska;fljewerwfjsl#@2'
test_user_email = 'testuser98@gmail.com'
test_context_name = 'JFKekeoo'
test_task_name = 'test_task_312FEW'
test_project_name = 'test_project_kljejar2'

class SeleniumTest(TestCase, StaticLiveServerTestCase):
    """
    This class tests the task functionalities of the task manager
    """

    # Setup and teardown
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(4)

        # Create a context object that can be used later
        test_superuser = User.objects.create_superuser(
            username=test_superuser_username,
            email=test_superuser_email,
            password=test_superuser_password,
        )
        test_context = Context.objects.create(
            name=test_context_name,
            user=User.objects.get(username=test_superuser_username)
        )
        test_task = Task.objects.create(
            name=test_task_name,
            created_by=test_superuser,
            supervisor=test_superuser
        )
        test_project = Project.objects.create(
            name=test_project_name,
            created_by=test_superuser,
            supervisor=test_superuser
        )

        # Relate these to each other
        test_task.context.add(test_context)

    def tearDown(self):
        self.browser.quit()

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


    def test_create_task_and_check_that_it_shows_up_in_the_task_manager_index_and_filter(self):
        # Create user
        self.user = User.objects.get(username=test_superuser_username)
        # Log the user in
        self.log_user_in(user_object=self.user, password=test_superuser_password)
        self.browser.implicitly_wait(10)
        # Pull up the main task manager page
        self.browser.get(str(self.live_server_url) + reverse('task_manager:index'))
        # Make sure we go to the task manager index
        task_index_url = str(self.live_server_url) + reverse('task_manager:index')
        self.browser.get(task_index_url)
        self.browser.implicitly_wait(4)
        self.assertTrue(str(task_index_url) == self.browser.current_url,
                        msg=('Assertion that current_url is %s failed. Current_url is %s' %
                             (str(reverse('task_manager:index')), self.browser.current_url)))
        # Click the 'add task' button on the sidebar
        self.browser.find_element_by_name('add_task_sidebar_link').click()
        # Assert that it takes us to the add task page
        self.assertTrue(str(reverse('task_manager:add_task')) in self.browser.current_url)
        # Fill out form
        name_input = self.browser.find_element_by_name('name')
        name_input.send_keys('Test Name BfC02@@')
        assigned_to_dropdown = Select(self.browser.find_element_by_name('assigned_to'))
        assigned_to_dropdown.select_by_visible_text(str(self.user))
        supervisor_dropdown = Select(self.browser.find_element_by_name('supervisor'))
        supervisor_dropdown.select_by_visible_text(str(self.user))
        context_input = Select(self.browser.find_element_by_name('context'))
        context_input.select_by_visible_text(str(test_context_name))
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

    def test_that_task_filter_works(self):
        # Get user and log in
        self.user = User.objects.get(username=test_superuser_username)
        # Log the user in
        self.log_user_in(user_object=self.user, password=test_superuser_password)
        self.browser.implicitly_wait(10)
        # Go to task index
        task_index_url = str(self.live_server_url) + reverse('task_manager:index')
        self.browser.get(task_index_url)
        self.assertTrue(str(task_index_url) == self.browser.current_url,
                        msg=('Assertion that current_url is %s failed. Current_url is %s' %
                             (str(reverse('task_manager:index')), self.browser.current_url)))
        # Fill out and submit task filter
        context_filter_input = Select(self.browser.find_element_by_name('context_filter'))
        context_filter_input.select_by_visible_text(test_context_name)
        type_task_or_project_filter = Select(self.browser.find_element_by_name('item_filter'))
        type_task_or_project_filter.select_by_visible_text('task')
        self.browser.find_element_by_name('task_filter_submit').click()
        # Quick check to make sure we're on the right page
        self.assertEqual(self.browser.current_url, str(self.live_server_url + reverse('task_manager:index')))
        # Now see if we see our task showing up
        task_table = self.browser.find_element_by_name('task_table')
        task_table_rows = task_table.find_elements_by_tag_name('tr')
        self.assertTrue(
            any(str(test_task_name) in row.text for row in task_table_rows),
            msg='The filter is not rendering a page showing the task'
        )

    def test_that_user_can_create_project(self):
        """
        This test starts with an already created task and project.
        The user creates the relationship between the task and project,
        then checks the details page of each to ensure that both show
        up on the other's page
        """
        # Constants
        local_test_project_name = 'Test_Project_29k23'

        # Get user and log in
        self.user = User.objects.get(username=test_superuser_username)
        # Log user in
        self.log_user_in(user_object=self.user, password=test_superuser_password)
        self.browser.implicitly_wait(4)
        # Go to task index
        task_index_url = str(self.live_server_url) + reverse('task_manager:index')
        self.browser.get(task_index_url)
        # Quick check to make sure we're on index page
        self.assertEqual(task_index_url, self.browser.current_url)
        # Now, go to add project page
        self.browser.find_element_by_name('create_project_sidebar_link').click()
        self.assertEqual(
            str(self.live_server_url + reverse('task_manager:add_project')),
            self.browser.current_url
        )
        # Fill out the add project form
        self.browser.find_element_by_name('name').send_keys(local_test_project_name)
        Select(self.browser.find_element_by_name('context')).select_by_visible_text(test_context_name)
        Select(self.browser.find_element_by_name('assigned_to')).select_by_visible_text(str(self.user))
        Select(self.browser.find_element_by_name('supervisor')).select_by_visible_text(str(self.user))
        self.browser.find_element_by_name('submit_created_project').click()
        # Now go to the index page to see if it appears
        self.browser.get(self.live_server_url + reverse('task_manager:index'))
        project_table = self.browser.find_element_by_name('project_table')
        project_table_rows = project_table.find_elements_by_tag_name('tr')
        self.assertTrue(
            any(str(local_test_project_name) in row.text for row in project_table_rows),
            msg="The Project Name is not rendering on the index after the task was created."
        )

    def test_that_tasks_related_to_projects_show_up(self):
        # Set variables to objects created in setUp
        local_test_task = Task.objects.get(name=test_task_name)
        local_test_project = Project.objects.get(name=test_project_name)
        self.user = User.objects.get(username=test_superuser_username)
        # Log the user in
        self.log_user_in(user_object=self.user, password=test_superuser_password)
        # Navigate to task details page
        self.browser.get(str(self.live_server_url + local_test_task.get_absolute_url()))
        # Click on the 'edit' button
        self.browser.find_element_by_name('edit_task_button').click()
        # Check to ensure we're on the task update page
        self.assertEqual(
                self.browser.current_url,
                str(self.live_server_url + reverse('task_manager:task_update', kwargs={'pk': local_test_task.pk}))
        )
        # Add the related project
        Select(self.browser.find_element_by_name('related_projects')).select_by_visible_text(test_project_name)
        # Click on the submit button
        self.browser.find_element_by_name('submit_task_edits').click()
        # Check to ensure it redirected to details page
        self.assertEqual(
            self.browser.current_url,
            str(self.live_server_url + reverse('task_manager:task_detail', kwargs={'pk': local_test_task.pk}))
        )
        # Assert that the project name shows up
        task_table = self.browser.find_element_by_name('individual_task_table')
        rows = task_table.find_elements_by_tag_name('tr')
        self.assertTrue(
            any(test_project_name in row.text for row in rows)
        )
        # TO DO: Navigate to project page, ensure it shows up there
        self.browser.get(
            reverse('task_manager:project_detail', kwargs={'pk': local_test_project.pk})
        )
        # Quick check to make sure we're on the project detail page
        self.assertEqual(
            self.browser.current_url,
            str(self.live_server_url + reverse('task_manager:project_detail', kwargs={'pk': local_test_project.pk})),
            msg=('self.browser.page_source is %s' %
                 (self.browser.page_source))
        )
        self.assertContains(response=self.browser.page_source, text=local_test_task.name)



if __name__ == '__main__':
    unittest.main(warnings='ignore')

