from django.test import Client, TestCase
from django.contrib.staticfiles.testing import LiveServerTestCase
from django.core.urlresolvers import reverse

from selenium import webdriver

import unittest


class SeleniumTests(TestCase, LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(5)

    def tearDown(self):
        self.browser.quit()

    def test_the_file_manager_index_redirected_anon_users(self):
        self.browser.get(self.live_server_url + reverse('file_manager:note_index'))
        # Check whether the browser goes to the login page.
        self.assertTrue(
            'login' in self.browser.current_url,
            msg='Current url is %s' % self.browser.current_url,
        )

if __name__ == '__main__':
    unittest.main(warnings='ignore')