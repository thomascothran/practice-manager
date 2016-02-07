from selenium import webdriver
import unittest

from django.core.urlresolvers import reverse
from django.test import TestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

class BasicTest(StaticLiveServerTestCase):
    """
    This class just checks to make sure that the basics of the task
    manager are up and working.
    """

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(4)

    def tearDown(self):
        self.browser.quit()

    def test_title(self):
        self.browser.get('http://localhost:8000/case-manager')
        self.assertIn('Cothran', self.browser.title)




if __name__ == '__main__':
    unittest.main(warnings='ignore')

