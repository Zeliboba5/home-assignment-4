from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import unittest
from urlparse import urlparse
from page_object import Page
import os


class MainPageTest(unittest.TestCase):
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

    def test_search(self):
        main_page = Page(self.driver)
        main_page.open()

        search_form = main_page.search_form
        search_form.wait_input_load()
        search_form.set_search_field(self.search_string)
        search_form.submit_search()
        result_search_string = search_form.get_result_search_string()

        self.assertTrue(main_page.is_domains_equal(search_form.get_current_url(), self.search_url))
        self.assertEquals(result_search_string, self.search_string)

    def test_right_ad_block_presence(self):
        ad_xpath = '//*[@id="slot_4499"]'

        main_page = Page(self.driver)
        main_page.open()
        self.assertTrue(main_page.is_element_present(ad_xpath))

    def test_center_ad_block_presence(self):
        ad_xpath = '//*[@id="slot_4847"]/a'

        main_page = Page(self.driver)
        main_page.open()
        self.assertTrue(main_page.is_element_present(ad_xpath))

    def test_search_bar_title(self):
        search_page_url = 'go.mail.ru'
        main_page = Page(self.driver)
        main_page.open()
        search_bar = main_page.search_bar_list
        search_bar.click_to_element_in_internet_bar()
        current_url = search_bar.get_current_url()
        result = current_url.find(search_page_url)

        self.assertNotEquals(result, -1)

    def test_search_bar_images(self):
        search_page_url = 'go.mail.ru'
        main_page = Page(self.driver)
        main_page.open()
        search_bar = main_page.search_bar_list
        search_bar.click_to_images_bar()
        current_url = search_bar.get_current_url()
        result = current_url.find(search_page_url)

        self.assertNotEquals(result, -1)

    def test_search_bar_video(self):
        search_page_url = 'go.mail.ru'
        main_page = Page(self.driver)
        main_page.open()
        search_bar = main_page.search_bar_list
        search_bar.click_to_video_bar()
        current_url = search_bar.get_current_url()
        result = current_url.find(search_page_url)

        self.assertNotEquals(result, -1)

    def test_search_bar_discussion(self):
        search_page_url = 'go.mail.ru'
        main_page = Page(self.driver)
        main_page.open()
        search_bar = main_page.search_bar_list
        search_bar.click_to_discussion_bar()
        current_url = search_bar.get_current_url()
        result = current_url.find(search_page_url)

        self.assertNotEquals(result, -1)

    def test_search_bar_answers(self):
        search_page_url = 'otvet.mail.ru'
        main_page = Page(self.driver)
        main_page.open()
        search_bar = main_page.search_bar_list
        search_bar.click_to_answers_bar()
        current_url = search_bar.get_current_url()
        result = current_url.find(search_page_url)

        self.assertNotEquals(result, -1)

    def test_my_world_ref(self):
        my_world_url = 'https://my.mail.ru/'

        main_page = Page(self.driver)
        main_page.open()

        left_ref_form = main_page.left_ref_form
        left_ref_form.open_my_world_ref()
        self.assertTrue(main_page.is_domains_equal(left_ref_form.get_current_url(), my_world_url))

    def test_left_form_gallery(self):
        main_page = Page(self.driver)
        main_page.open()

        left_ref_form = main_page.left_ref_form
        left_ref_form.wait_gallery_load()
        self.assertTrue(left_ref_form.is_element_present(left_ref_form.MY_WORLD_GALLERY))


class PersonalInfoTestCase(MainPageTest):
    login = "tester-mega"
    second_login = "tester-mega2"
    username = "Mega Tester"
    password = os.environ['TTHA4PASSWORD']
    wrong_password = "qwerty123"
    user_email = "tester-mega@mail.ru"

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

    def test_account_menu_open(self):
        main_page = Page(self.driver)
        main_page.open()
        auth_form = main_page.auth_form

        auth_form.login(self.login, self.password)
        account_menu = main_page.account_menu

        account_menu.open_account_menu()

    def test_account_menu_info(self):
        main_page = Page(self.driver)
        main_page.open()
        auth_form = main_page.auth_form

        auth_form.login(self.login, self.password)
        account_menu = main_page.account_menu

        account_menu.open_account_menu()
        self.assertEqual(self.username, account_menu.get_username_from_account_menu())
        self.assertEqual(self.user_email, account_menu.get_email_from_account_menu())

    def test_account_menu_second_email(self):
        main_page = Page(self.driver)
        main_page.open()
        auth_form = main_page.auth_popup_form
        auth_form.open_login_popup()

        auth_form.login(self.login, self.password)
        account_menu = main_page.account_menu

        account_menu.open_account_menu()

        account_menu.add_second_email()
        auth_form.login(self.second_login, self.password)

        account_menu.open_account_menu()
        self.assertTrue(account_menu.is_both_emails_present())

    def test_mailbox_info(self):
        main_page = Page(self.driver)
        main_page.open()

        auth_form = main_page.auth_popup_form
        auth_form.open_login_popup()
        auth_form.login(self.login, self.password)
        main_page.open()

        mailbox_form = main_page.mailbox_form
        self.assertEqual(mailbox_form.get_user_email(), self.user_email)

    def test_mailbox_add_second_email(self):
        main_page = Page(self.driver)
        main_page.open()

        auth_form = main_page.auth_popup_form
        auth_form.open_login_popup()
        auth_form.login(self.login, self.password)
        main_page.open()

        mailbox_form = main_page.mailbox_form
        mailbox_form.open_email_dropdown()
        mailbox_form.add_new_email()
        auth_form.login(self.second_login, self.password)
        main_page.open()
        mailbox_form.open_email_dropdown()
        self.assertTrue(mailbox_form.is_both_emails_present())


class TopBarTest(MainPageTest):
    def test_top_bar_dropdown(self):
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

    def test_top_bar_presence(self):
        main_page = Page(self.driver)
        main_page.open()

        top_bar_form = main_page.top_bar_form

        self.assertTrue(top_bar_form.is_element_present(top_bar_form.TOP_BAR))

    def test_top_bar_email_ref(self):
        mail_url = 'https://e.mail.ru/'
        main_page = Page(self.driver)
        main_page.open()

        top_bar_form = main_page.top_bar_form

        top_bar_form.go_to_mail_by_top_bar_ref()
        self.assertTrue(main_page.is_domains_equal(top_bar_form.get_current_url(), mail_url))


class NewsBlockTest(MainPageTest):
    def test_description_presence(self):
        main_page = Page(self.driver)
        main_page.open()

        main_page.set_full_screen_size()  # Description only visible on full size
        news_form = main_page.news_form
        self.assertTrue(news_form.is_news_description_visible())

    def test_title_and_description_relation(self):
        main_page = Page(self.driver)
        main_page.open()

        main_page.set_full_screen_size()
        news_form = main_page.news_form
        self.assertTrue(news_form.is_description_related_to_news())

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



