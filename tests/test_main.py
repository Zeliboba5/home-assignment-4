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
    MAIL_RU_REF = '//*[@id="portal-menu"]/div[2]/div/div[1]/div[1]/div/div/a/img'

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
        WebDriverWait(self.driver, 5).until(
            lambda driver: EC.element_to_be_clickable(driver.find_element_by_xpath(self.LOGIN_BUTTON))
        )
        self.driver.find_element_by_xpath(self.LOGIN_BUTTON).click()
        WebDriverWait(self.driver, 5).until(
            lambda driver: EC.element_to_be_clickable(driver.find_element_by_xpath(self.LOGIN_INPUT))
        )


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
    POPUP_PATH = '//*[@id="PH_projectsMenu"]'
    POPUP_BUTTON = '//*[@id="PH_projectsMenu_button"]'

    def __init__(self, driver):
        self.driver = driver

    def get_user_email(self):
        return WebDriverWait(self.driver, 10).until(
            lambda driver: driver.find_element_by_xpath(self.EMAIL_FORM).text
        )

    def trigger_popup(self):
        WebDriverWait(self.driver, 5).until(
            lambda driver: EC.element_to_be_clickable(driver.find_element_by_xpath(self.POPUP_BUTTON))
        )
        self.driver.find_element_by_xpath(self.POPUP_BUTTON).click()

    def get_popup_classes(self):
        return self.driver.find_element_by_xpath(self.POPUP_PATH).get_attribute("class").split()


class SearchForm(object):
    SEARCH_INPUT = '//*[@id="q"]'
    SEARCH_SUBMIT = '//*[@id="search__button__wrapper__field"]'
    SEARCH_REF = '//*[@id="logo"]/img'  # Don't know if i should test this

    def __init__(self, driver):
        self.driver = driver

    def get_current_url(self):
        return self.driver.current_url

    def set_search_field(self, search_string):
        WebDriverWait(self.driver, 5).until(
            lambda driver: EC.element_to_be_clickable(driver.find_element_by_xpath(self.SEARCH_INPUT))
        )
        self.driver.find_element_by_xpath(self.SEARCH_INPUT).send_keys(search_string)

    def submit_search(self):
        WebDriverWait(self.driver, 5).until(
            lambda driver: EC.element_to_be_clickable(driver.find_element_by_xpath(self.SEARCH_SUBMIT))
        )
        self.driver.find_element_by_xpath(self.SEARCH_SUBMIT).click()
        WebDriverWait(self.driver, 5).until(
            lambda driver: EC.presence_of_element_located(driver.find_element_by_xpath(self.SEARCH_REF))
        )

    def get_result_search_string(self):
        return WebDriverWait(self.driver, 10).until(
            lambda driver: driver.find_element_by_xpath(self.SEARCH_INPUT).get_attribute('value').encode('utf-8')
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

    def test_login_by_popup(self):
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

    def get_parent_element(self, xpath_to_element):
        element = self.driver.find_element_by_xpath(xpath_to_element)
        return element.find_element_by_xpath('..')

    def test_news_blocks(self):
        not_chosen_block_class = 'news__list '.split()
        chosen_block_class = 'news__list  news__list_active'.split()

        news_block_button = '//*[@id="news"]/div[1]/table/tbody/tr/td['
        string_end = ']'
        news_block_path = '//*[@id="news__wrap"]/div['

        main_page = Page(self.driver)
        main_page.open()

        self.driver.set_window_size(800, 500)

        blocks_number = 5

        for i in range(1, blocks_number):
            element = self.driver.find_element_by_xpath(news_block_path + str(i + 1) + string_end)
            self.assertEquals(element.get_attribute("class").split(), chosen_block_class)
            self.driver.find_element_by_xpath(news_block_button + str(i + 1) + string_end).click()
            self.assertEquals(element.get_attribute("class").split(), not_chosen_block_class)

        self.driver.set_window_size(1300, 800)
        self.driver.find_element_by_xpath(news_block_button + str(1) + string_end).click()

        blocks_number = 8

        for i in range(1, blocks_number):
            element = self.driver.find_element_by_xpath(news_block_path + str(i + 1) + string_end)
            self.assertEquals(element.get_attribute("class").split(), chosen_block_class)
            self.driver.find_element_by_xpath(news_block_button + str(i + 1) + string_end).click()
            self.assertEquals(element.get_attribute("class").split(), not_chosen_block_class)

    def test_top_bar_popup(self):
        popup_closed_classes = 'x-ph__menu'.split()
        popup_opened_classes_full_size = 'x-ph__menu x-ph__menu_open x-ph__menu_open_left'.split()
        popup_opened_classes_small_size = 'x-ph__menu x-ph__menu_open x-ph__menu_open_right'.split()
        main_page = Page(self.driver)
        main_page.open()

        top_bar_form = main_page.top_bar_form

        self.driver.set_window_size(800, 500)

        self.assertEquals(top_bar_form.get_popup_classes(), popup_closed_classes)
        top_bar_form.trigger_popup()
        self.assertEquals(top_bar_form.get_popup_classes(), popup_opened_classes_small_size)
        top_bar_form.trigger_popup()
        self.assertEquals(top_bar_form.get_popup_classes(), popup_closed_classes)

        self.driver.set_window_size(1300, 800)

        self.assertEquals(top_bar_form.get_popup_classes(), popup_closed_classes)
        top_bar_form.trigger_popup()
        self.assertEquals(top_bar_form.get_popup_classes(), popup_opened_classes_full_size)
        top_bar_form.trigger_popup()
        self.assertEquals(top_bar_form.get_popup_classes(), popup_closed_classes)
