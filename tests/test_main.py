from selenium import webdriver

import unittest
import urlparse

class Page(object):
	BASE_URL = "http://mail.ru"
	URI = ""

	def __init__(self, driver):
		self.driver = driver

	def open(self):
		url = urlparse.urljoin(self.BASE_URL, self.URI)
		self.driver.get(url)


class MainPageTest(unittest.TestCase):
	def setUp(self):
		self.driver = webdriver.Firefox()

	def tearDown(self):
		self.driver.quit()

	def testOpen(self):
		mainPage = Page(self.driver)
		mainPage.open()
