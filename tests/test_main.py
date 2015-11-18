from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import unittest
from selenium.webdriver.support import expected_conditions as EC
from urlparse import urlparse
import os


class Page(object):
    BASE_URL = "http://mail.ru"

    def __init__(self, driver):
        self.driver = driver

    def open(self):
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

    @property
    def search_form(self):
        return SearchForm(self.driver)

    @property
    def auth_popup_form(self):
        return AuthPopupForm(self.driver)


class AuthForm(object):
    LOGIN_INPUT = '//*[@id="mailbox__login"]'
    PASSWORD_INPUT = '//*[@id="mailbox__password"]'
    SUBMIT_BUTTON = '//*[@id="mailbox__auth__button"]'
    MAIL_RU_REF = '//*[@id="portal-headline"]/table/tbody/tr/td[1]/a[1]'

    def __init__(self, driver):
        self.driver = driver

    def set_login(self, login):
        self.driver.find_element_by_xpath(self.LOGIN_INPUT).send_keys(login)

    def set_password(self, password):
        self.driver.find_element_by_xpath(self.PASSWORD_INPUT).send_keys(password)

    def submit(self):
        self.driver.find_element_by_xpath(self.SUBMIT_BUTTON).click()
        WebDriverWait(self.driver, 5).until(
            lambda driver: EC.presence_of_element_located(driver.find_element_by_xpath(self.MAIL_RU_REF))
        )


class AuthPopupForm(AuthForm):
    LOGIN_INPUT = '//*[@id="ph_login"]'
    PASSWORD_INPUT = '//*[@id="ph_password"]'
    SUBMIT_BUTTON = '//*[@id="x-ph__authForm__popup"]/div[3]/div/div[1]/span/span/input'
    LOGIN_BUTTON = '//*[@id="PH_authLink"]'

    def open_login_popup(self):
        self.driver.find_element_by_xpath(self.LOGIN_BUTTON).click()


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


class SearchForm(object):
    SEARCH_INPUT = '//*[@id="q"]'
    SEARCH_SUBMIT = '//*[@id="search__button__wrapper__field"]'
    RESULT_SEARCH_INPUT = '//*[@id="q"]'  # Don't know if i should test this

    def __init__(self, driver):
        self.driver = driver

    def get_current_url(self):
        return self.driver.current_url

    def set_search_field(self, search_string):
        self.driver.find_element_by_xpath(self.SEARCH_INPUT).send_keys(search_string)

    def submit_search(self):
        self.driver.find_element_by_xpath(self.SEARCH_SUBMIT).click()
        WebDriverWait(self.driver, 5).until(
            lambda driver: EC.presence_of_element_located(driver.find_element_by_xpath(self.RESULT_SEARCH_INPUT))
        )

    def get_result_search_string(self):
        return WebDriverWait(self.driver, 10).until(
            lambda driver: driver.find_element_by_xpath(self.RESULT_SEARCH_INPUT).get_attribute('value').encode('utf-8')
        )


class MainPageTest(unittest.TestCase):
    SEARCH_INPUT = '//*[@id="q"]'
    login = "tester-mega"
    password = os.environ['MAIL_TEST_PASS']
    user_email = "tester-mega@mail.ru"
    search_string = "test"
    search_url = "http://go.mail.ru/"

    def setUp(self):
        self.driver = webdriver.Firefox()

    def tearDown(self):
        self.driver.quit()

    def test_user_login(self):
        main_page = Page(self.driver)
        main_page.open()

        auth_form = main_page.auth_form
        auth_form.set_login(self.login)
        auth_form.set_password(self.password)
        auth_form.submit()

        main_page.open()

        user_info_form = main_page.user_info_form
        user_email = user_info_form.get_user_email()
        self.assertEquals(user_email, self.user_email)

        top_bar_form = main_page.top_bar_form
        user_email = top_bar_form.get_user_email()
        self.assertEquals(user_email, self.user_email)

    def test_search(self):
        main_page = Page(self.driver)
        main_page.open()
        WebDriverWait(self.driver, 5).until(
            lambda driver: EC.visibility_of(driver.find_element_by_xpath(self.SEARCH_INPUT))
        )

        search_form = main_page.search_form
        search_form.set_search_field(self.search_string)
        search_form.submit_search()
        result_search_string = search_form.get_result_search_string()

        full_search_url = search_form.get_current_url()
        full_search_url = urlparse(full_search_url)
        search_url = '{uri.scheme}://{uri.netloc}/'.format(uri=full_search_url)

        self.assertEquals(result_search_string, self.search_string)
        self.assertEquals(search_url, self.search_url)

    def testLoginByPopup(self):
        main_page = Page(self.driver)
        main_page.open()

        auth_form = main_page.auth_popup_form
        auth_form.open_login_popup()
        auth_form.set_login(self.login)
        auth_form.set_password(self.password)
        auth_form.submit()

        main_page.open()

        user_info_form = main_page.user_info_form
        user_email = user_info_form.get_user_email()
        self.assertEquals(user_email, self.user_email)

        top_bar_form = main_page.top_bar_form
        user_email = top_bar_form.get_user_email()
        self.assertEquals(user_email, self.user_email)
