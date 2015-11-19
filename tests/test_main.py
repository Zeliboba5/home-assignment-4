from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
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

    def set_small_screen_size(self):
        width = 1000  # 1150 and 1250 are border lines between changes in design
        height = 700  # doesn't affect functionality

        self.driver.set_window_size(width, height)

    def set_full_screen_size(self):
        width = 1300  # 1150 and 1250 are border lines between changes in design
        height = 700  # doesn't affect functionality

        self.driver.set_window_size(width, height)

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

    @property
    def news_form(self):
        return NewsForm(self.driver)


class AuthForm(object):
    LOGIN_INPUT = '//*[@id="mailbox__login"]'
    PASSWORD_INPUT = '//*[@id="mailbox__password"]'
    SUBMIT_BUTTON = '//*[@id="mailbox__auth__button"]'
    MAIL_RU_REF = '//*[@id="portal-menu"]/div[2]/div/div[1]/div[1]/div/div/a/img'
    ERROR_MESSAGE_PATH = '//*[@id="LoginExternal"]/div[1]/div[3]'

    def __init__(self, driver):
        self.driver = driver

    def set_login(self, login):
        WebDriverWait(self.driver, 5).until(
            lambda driver: EC.element_to_be_clickable(driver.find_element_by_xpath(self.LOGIN_INPUT))
        )
        self.driver.find_element_by_xpath(self.LOGIN_INPUT).send_keys(login)

    def set_password(self, password):
        WebDriverWait(self.driver, 5).until(
            lambda driver: EC.element_to_be_clickable(driver.find_element_by_xpath(self.PASSWORD_INPUT))
        )
        self.driver.find_element_by_xpath(self.PASSWORD_INPUT).send_keys(password)

    def submit(self):
        self.driver.find_element_by_xpath(self.SUBMIT_BUTTON).click()
        WebDriverWait(self.driver, 5).until(
            lambda driver: EC.presence_of_element_located(driver.find_element_by_xpath(self.MAIL_RU_REF))
        )

    def get_error_message_classes(self):
        return self.driver.find_element_by_xpath(self.ERROR_MESSAGE_PATH).get_attribute("class").split()


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


class NewsForm(object):
    def __init__(self, driver):
        self.driver = driver

    def get_news_block_classes(self, span_index):
        news_block_path = '//*[@id="news__wrap"]/div[' + str(span_index) + ']'
        return self.driver.find_element_by_xpath(news_block_path).get_attribute("class").split()

    def click_news_block_button(self, span_index):
        news_block_button = '//*[@id="news"]/div[1]/table/tbody/tr/td[' + str(span_index) + ']'
        self.driver.find_element_by_xpath(news_block_button).click()

    def set_news_block_to_default(self):
        news_block_button = '//*[@id="news"]/div[1]/table/tbody/tr/td[1]'
        self.driver.find_element_by_xpath(news_block_button).click()


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
    SEARCH_REF = '//*[@id="logo"]/img'

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
        WebDriverWait(self.driver, 5).until(  # This wait is to ensure that page has changed, because search
            lambda driver: EC.presence_of_element_located(driver.find_element_by_xpath(self.SEARCH_REF))
            # input have same path on all pages
        )
        WebDriverWait(self.driver, 5).until(
            lambda driver: EC.element_to_be_clickable(driver.find_element_by_xpath(self.SEARCH_INPUT))
        )

    def get_result_search_string(self):  # Don't know if i should test this
        return WebDriverWait(self.driver, 10).until(
            lambda driver: driver.find_element_by_xpath(self.SEARCH_INPUT).get_attribute('value').encode('utf-8')
        )


class MainPageTest(unittest.TestCase):
    SEARCH_INPUT = '//*[@id="q"]'
    login = "tester-mega"
    password = os.environ['MAIL_TEST_PASS']
    wrong_password = "qwerty123"
    user_email = "tester-mega@mail.ru"
    search_string = "test"
    search_url = "http://go.mail.ru/"

    def setUp(self):
        self.driver = webdriver.Remote(
            command_executor='http://127.0.0.1:4444/wd/hub',
            desired_capabilities=DesiredCapabilities.CHROME,
        )

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

    def test_user_login_fail(self):
        error_message_classes = ('login-page__external_error' +
                                 ' login-page__external__text_indent js-login-page__external__info').split()

        main_page = Page(self.driver)
        main_page.open()

        auth_form = main_page.auth_form
        auth_form.set_login(self.login)
        auth_form.set_password(self.wrong_password)
        auth_form.submit()

        self.assertEqual(auth_form.get_error_message_classes(), error_message_classes)

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

        main_page = Page(self.driver)
        main_page.open()
        news_form = main_page.news_form

        main_page.set_small_screen_size()

        blocks_number = 4

        for i in range(2, blocks_number + 1):  # starts from 2 because of unique main page layout
            self.assertEquals(news_form.get_news_block_classes(i), chosen_block_class)
            news_form.click_news_block_button(i)
            self.assertEquals(news_form.get_news_block_classes(i), not_chosen_block_class)

        main_page.set_full_screen_size()
        news_form.set_news_block_to_default()

        blocks_number = 7

        for i in range(2, blocks_number + 1):
            self.assertEquals(news_form.get_news_block_classes(i), chosen_block_class)
            news_form.click_news_block_button(i)
            self.assertEquals(news_form.get_news_block_classes(i), not_chosen_block_class)

    def test_top_bar_popup(self):
        popup_closed_classes = 'x-ph__menu'.split()
        popup_opened_classes_full_size = 'x-ph__menu x-ph__menu_open x-ph__menu_open_left'.split()
        popup_opened_classes_small_size = 'x-ph__menu x-ph__menu_open x-ph__menu_open_right'.split()
        main_page = Page(self.driver)
        main_page.open()

        top_bar_form = main_page.top_bar_form

        main_page.set_small_screen_size()

        self.assertEquals(top_bar_form.get_popup_classes(), popup_closed_classes)
        top_bar_form.trigger_popup()
        self.assertEquals(top_bar_form.get_popup_classes(), popup_opened_classes_small_size)
        top_bar_form.trigger_popup()
        self.assertEquals(top_bar_form.get_popup_classes(), popup_closed_classes)

        main_page.set_full_screen_size()

        self.assertEquals(top_bar_form.get_popup_classes(), popup_closed_classes)
        top_bar_form.trigger_popup()
        self.assertEquals(top_bar_form.get_popup_classes(), popup_opened_classes_full_size)
        top_bar_form.trigger_popup()
        self.assertEquals(top_bar_form.get_popup_classes(), popup_closed_classes)


class DebugPageTest(unittest.TestCase):
    SEARCH_INPUT = '//*[@id="q"]'
    login = "tester-mega"
    password = os.environ['MAIL_TEST_PASS']
    wrong_password = "qwerty123"
    user_email = "tester-mega@mail.ru"
    search_string = "test"
    search_url = "http://go.mail.ru/"

    def setUp(self):
        self.driver = webdriver.Remote(
            command_executor='http://127.0.0.1:4444/wd/hub',
            desired_capabilities=DesiredCapabilities.FIREFOX,
        )

    def tearDown(self):
        self.driver.quit()

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
