from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import unittest
import urlparse
import os


class Page(object):
    BASE_URL = "http://mail.ru"
    URI = ""

    def __init__(self, driver):
        self.driver = driver

    def open(self):
        url = urlparse.urljoin(self.BASE_URL, self.URI)
        self.driver.get(url)

    def go_back_to_main(self):
        self.driver.get(self.BASE_URL)

    @property
    def auth_form(self):
        return AuthForm(self.driver)

    @property
    def user_info_form(self):
        return UserInfoForm(self.driver)

    @property
    def top_bar_form(self):
        return TopBarForm(self.driver)


class AuthForm(object):
    LOGIN_INPUT = '//*[@id="mailbox__login"]'
    PASSWORD_INPUT = '//*[@id="mailbox__password"]'
    SUBMIT_BUTTON = '//*[@id="mailbox__auth__button"]'

    def __init__(self, driver):
        self.driver = driver

    def set_login(self, login):
        self.driver.find_element_by_xpath(self.LOGIN_INPUT).send_keys(login)

    def set_password(self, password):
        self.driver.find_element_by_xpath(self.PASSWORD_INPUT).send_keys(password)

    def submit(self):
        self.driver.find_element_by_xpath(self.SUBMIT_BUTTON).click()


class UserInfoForm(object):
    EMAIL_FORM = '//*[@id="js-mailbox-user"]'

    def __init__(self, driver):
        self.driver = driver

    def get_user_email(self):
        return WebDriverWait(self.driver, 10).until(
            lambda driver: driver.find_element_by_xpath(self.EMAIL_FORM).text
        )


class TopBarForm(object):
    EMAIL_FORM = '//*[@id="PH_user-email"]'

    def __init__(self, driver):
        self.driver = driver

    def get_user_email(self):
        return WebDriverWait(self.driver, 10).until(
            lambda driver: driver.find_element_by_xpath(self.EMAIL_FORM).text
        )


class MainPageTest(unittest.TestCase):
    login = "tester-mega"
    password = os.environ['MAIL_TEST_PASS']
    user_email = "tester-mega@mail.ru"

    def setUp(self):
        self.driver = webdriver.Firefox()

    def tearDown(self):
        self.driver.quit()

    def testUserLogin(self):
        main_page = Page(self.driver)
        main_page.open()

        auth_form = main_page.auth_form
        auth_form.set_login(self.login)
        auth_form.set_password(self.password)
        auth_form.submit()

        main_page.go_back_to_main()

        user_info_form = main_page.user_info_form
        user_email = user_info_form.get_user_email()
        self.assertEquals(user_email, self.user_email)

        top_bar_form = main_page.top_bar_form
        user_email = top_bar_form.get_user_email()
        self.assertEquals(user_email, self.user_email)
