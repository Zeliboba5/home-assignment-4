from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
import unittest
from selenium.webdriver.support import expected_conditions as EC
from urlparse import urlparse
from page_object import Page
import os


class MainPageTest(unittest.TestCase):
    SEARCH_INPUT = '//*[@id="q"]'
    login = "tester-mega"
    password = os.environ['TTHA4PASSWORD']
    wrong_password = "qwerty123"
    user_email = "tester-mega@mail.ru"
    search_string = "test"
    search_url = "http://go.mail.ru/"
    browser = os.environ['TTHA4BROWSER']

    def setUp(self):
        if self.browser == 'CHROME':
            capabilities = DesiredCapabilities.CHROME
        elif self.browser == 'FIREFOX':
            capabilities = DesiredCapabilities.FIREFOX
        else:
            capabilities = DesiredCapabilities.FIREFOX

        self.driver = webdriver.Remote(
            command_executor='http://127.0.0.1:4444/wd/hub',
            desired_capabilities=capabilities,
        )

    def tearDown(self):
        self.driver.quit()

    def test_user_login_and_logout(self):
        main_page = Page(self.driver)
        main_page.open()

        auth_form = main_page.auth_form
        auth_form.login(self.login, self.password)

        main_page.open()

        user_info_form = main_page.user_info_form
        user_email = user_info_form.get_user_email()
        self.assertEquals(user_email, self.user_email)

        top_bar_form = main_page.top_bar_form
        user_email = top_bar_form.get_user_email()
        self.assertEquals(user_email, self.user_email)

        auth_form.logout()

        self.assertTrue(auth_form.is_auth_input_present())

    def test_user_login_fail(self):
        error_message_classes = ('login-page__external_error' +
                                 ' login-page__external__text_indent js-login-page__external__info').split()

        main_page = Page(self.driver)
        main_page.open()

        auth_form = main_page.auth_form
        auth_form.login(self.login, self.wrong_password)

        self.assertEqual(auth_form.get_error_message_classes(), error_message_classes)

    def test_search(self):
        main_page = Page(self.driver)
        main_page.open()

        search_form = main_page.search_form
        search_form.wait_input_load()
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
        auth_form.login(self.login, self.password)

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
