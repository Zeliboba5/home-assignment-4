# coding=utf-8
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By


class Page(object):
    BASE_URL = "http://mail.ru"

    def __init__(self, driver):
        self.driver = driver

    def open(self):
        self.driver.get(self.BASE_URL)

    def set_small_screen_size(self):
        width = 1000  # 11100 and 12100 are border lines between changes in design
        height = 700  # doesn't affect functionality

        self.driver.set_window_size(width, height)

    def set_full_screen_size(self):
        width = 1300  # 11100 and 12100 are border lines between changes in design
        height = 700  # doesn't affect functionality

        self.driver.set_window_size(width, height)

    def is_element_present(self, path):
        element = WebDriverWait(self.driver, 10).until(
            lambda driver: driver.find_element_by_xpath(path)
        )

        if element.is_displayed():
            return True
        else:
            return False

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

    @property
    def account_menu(self):
        return AccountMenu(self.driver)

    @property
    def mailbox_form(self):
        return MailboxForm(self.driver)


class Form(object):
    def __init__(self, driver):
        self.driver = driver

    def is_element_present(self, path):
        element = WebDriverWait(self.driver, 10).until(
            lambda driver: driver.find_element_by_xpath(path)
        )

        if element.is_displayed():
            return True
        else:
            return False

    def get_current_url(self):
        return self.driver.current_url


class AuthForm(Form):
    LOGIN_INPUT = '//*[@id="mailbox__login"]'
    PASSWORD_INPUT = '//*[@id="mailbox__password"]'
    SUBMIT_BUTTON = '//*[@id="mailbox__auth__button"]'
    MAIL_RU_REF = '//*[@id="portal-menu"]/div[2]/div/div[1]/div[1]/div/div/a/img'
    ERROR_MESSAGE_PATH = '//*[@id="LoginExternal"]/div[1]/div[3]'
    LOGOUT_BUTTON = '//*[@id="PH_logoutLink"]'

    def login(self, login, password):
        self.set_login(login)
        self.set_password(password)
        self.submit()

    def set_login(self, login):
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, self.LOGIN_INPUT))
        )
        self.driver.find_element_by_xpath(self.LOGIN_INPUT).send_keys(login)

    def set_password(self, password):
        WebDriverWait(self.driver, 10).until(
            lambda driver: EC.visibility_of((By.XPATH, self.PASSWORD_INPUT))
        )
        self.driver.find_element_by_xpath(self.PASSWORD_INPUT).send_keys(password)

    def submit(self):
        self.driver.find_element_by_xpath(self.SUBMIT_BUTTON).click()
        WebDriverWait(self.driver, 10).until(
            lambda driver: EC.element_to_be_clickable(driver.find_element_by_xpath(self.MAIL_RU_REF))
        )

    def get_error_message_classes(self):
        return self.driver.find_element_by_xpath(self.ERROR_MESSAGE_PATH).get_attribute("class").split()

    def logout(self):
        self.driver.find_element_by_xpath(self.LOGOUT_BUTTON).click()

    def is_auth_input_present(self):
        return WebDriverWait(self.driver, 10).until(
            lambda driver: driver.find_element_by_xpath(self.LOGIN_INPUT).is_displayed()
        )


class AuthPopupForm(AuthForm):
    LOGIN_INPUT = '//*[@id="ph_login"]'
    PASSWORD_INPUT = '//*[@id="ph_password"]'
    SUBMIT_BUTTON = '//*[@id="x-ph__authForm__popup"]/div[3]/div/div[1]/span/span/input'
    LOGIN_BUTTON = '//*[@id="PH_authLink"]'
    LOGIN_POPUP = '//*[@id="x-ph__authForm__popup"]'
    LOGIN_FORM = '//*[@id="x-ph__authForm"]/div'
    PRELOADER = '//*[@class="x-ph__popup__content__preloader"]'

    def open_login_popup(self):
        element = WebDriverWait(self.driver, 10).until(
            lambda driver: driver.find_element_by_xpath(self.LOGIN_BUTTON)
        )
        element.click()
        WebDriverWait(self.driver, 10).until(
            lambda driver: driver.find_element_by_xpath(self.LOGIN_FORM)
        )
        WebDriverWait(self.driver, 10).until(
            lambda driver: EC.invisibility_of_element_located(driver.find_element_by_xpath(self.PRELOADER))
        )


class NewsForm(Form):
    # Эти селекторы подходят, так как нас интересуют только первые элементы
    news_description = '//a[@class="news__list__item__description"]'
    news_title = '//a[@class="news__list__item__link"]'
    NEWS_BLOCKS = ['//*[@data-n="main"]',
                   '//*[@data-n="sport"]',
                   '//*[@data-n="auto"]',
                   '//*[@data-n="afisha"]',
                   '//*[@data-n="lady"]',
                   '//*[@data-n="games"]',
                   '//*[@data-n="hitech"]']

    def get_news_block_classes(self, span_index):
        news_block_path = '//*[@id="news__wrap"]/div[' + str(span_index) + ']'
        return self.driver.find_element_by_xpath(news_block_path).get_attribute("class").split()

    def click_news_block_button(self, span_index):
        news_block_button = self.NEWS_BLOCKS[span_index-1]
        self.driver.find_element_by_xpath(news_block_button).click()

    def set_news_block_to_default(self):
        news_block_button = self.NEWS_BLOCKS[0]
        self.driver.find_element_by_xpath(news_block_button).click()

    def is_news_description_visible(self):
        element = WebDriverWait(self.driver, 10).until(
            lambda driver: driver.find_element_by_xpath(self.news_description)
        )

        if element.is_displayed():
            return True
        else:
            return False

    def is_description_related_to_news(self):
        title_number = WebDriverWait(self.driver, 10).until(
            lambda driver: driver.find_element_by_xpath(self.news_title).get_attribute("name")
        )
        description_number = WebDriverWait(self.driver, 10).until(
            lambda driver: driver.find_element_by_xpath(self.news_description).get_attribute("name")
        )

        if description_number == title_number:
            return True
        else:
            return False


class UserInfoForm(Form):
    EMAIL_FORM = '//*[@id="js-mailbox-user"]'

    def get_user_email(self):
        return WebDriverWait(self.driver, 10).until(
            lambda driver: driver.find_element_by_xpath(self.EMAIL_FORM).text
        )


class TopBarForm(Form):
    EMAIL_FORM = '//*[@id="PH_user-email"]'
    POPUP_PATH = '//*[@id="PH_projectsMenu"]'
    POPUP_BUTTON = '//*[@id="PH_projectsMenu_button"]'
    TOP_BAR = '//*[@id="portal-headline"]'
    EMAIL_REF = '//*[@id="ph_mail"]'
    EMAIL_MENU = '//*[@id="portal-menu"]'

    def get_user_email(self):
        return WebDriverWait(self.driver, 10).until(
            lambda driver: driver.find_element_by_xpath(self.EMAIL_FORM).text
        )

    def trigger_popup(self):
        WebDriverWait(self.driver, 10).until(
            lambda driver: EC.element_to_be_clickable(driver.find_element_by_xpath(self.POPUP_BUTTON))
        )
        self.driver.find_element_by_xpath(self.POPUP_BUTTON).click()

    def get_popup_classes(self):
        return self.driver.find_element_by_xpath(self.POPUP_PATH).get_attribute("class").split()

    def go_to_mail_by_top_bar_ref(self):
        WebDriverWait(self.driver, 10).until(
            lambda driver: EC.element_to_be_clickable(driver.find_element_by_xpath(self.EMAIL_REF))
        )
        self.driver.find_element_by_xpath(self.EMAIL_REF).click()
        WebDriverWait(self.driver, 10).until(
            lambda driver: EC.element_to_be_clickable(driver.find_element_by_xpath(self.EMAIL_MENU))
        )


class SearchForm(Form):
    SEARCH_INPUT = '//*[@id="q"]'
    SEARCH_SUBMIT = '//*[@id="search__button__wrapper__field"]'
    SEARCH_REF = '//*[@class="pm-logo__link"]'

    def wait_input_load(self):
        WebDriverWait(self.driver, 10).until(
            lambda driver: EC.visibility_of(driver.find_element_by_xpath(self.SEARCH_INPUT))
        )

    def set_search_field(self, search_string):
        WebDriverWait(self.driver, 10).until(
            lambda driver: EC.element_to_be_clickable(driver.find_element_by_xpath(self.SEARCH_INPUT))
        )
        self.driver.find_element_by_xpath(self.SEARCH_INPUT).send_keys(search_string)

    def submit_search(self):
        WebDriverWait(self.driver, 10).until(
            lambda driver: EC.element_to_be_clickable(driver.find_element_by_xpath(self.SEARCH_SUBMIT))
        )
        self.driver.find_element_by_xpath(self.SEARCH_SUBMIT).click()
        WebDriverWait(self.driver, 10).until(  # This wait is to ensure that page has changed, because search
            lambda driver: EC.presence_of_element_located(driver.find_element_by_xpath(self.SEARCH_REF))
            # input have same path on all pages
        )
        WebDriverWait(self.driver, 10).until(
            lambda driver: EC.element_to_be_clickable(driver.find_element_by_xpath(self.SEARCH_INPUT))
        )

    def get_result_search_string(self):  # Don't know if i should test this
        return WebDriverWait(self.driver, 10).until(
            lambda driver: driver.find_element_by_xpath(self.SEARCH_INPUT).get_attribute('value').encode('utf-8')
        )


class AccountMenu(Form):
    account_menu = '//*[@id="PH_authMenu"]'
    account_menu_username = '//div[@class="x-ph__auth_list__item__info__email__text"]'
    account_menu_email = '//div[@class="x-ph__auth_list__item__info__text"]'
    account_menu_button = '//*[@id="PH_authMenu_button"]'
    account_menu_add_email = '//*[@id="PH_loginAnotherLink"]'
    account_menu_first_email_block = '//*[@id="PH_authMenu_links"]'
    account_menu_second_email_block = '//*[@id="PH_authMenu_list_wrap"]'
    LOGIN_POPUP = '//*[@id="x-ph__authForm__popup"]'

    def is_popup_opened(self):
        element = self.driver.find_element_by_xpath(self.account_menu)
        if element.is_displayed():
            return True
        else:
            return False

    def open_account_menu(self):
        WebDriverWait(self.driver, 10).until(
            lambda driver: EC.element_to_be_clickable(driver.find_element_by_xpath(self.account_menu_button))
        )
        self.driver.find_element_by_xpath(self.account_menu_button).click()
        WebDriverWait(self.driver, 10).until(
            lambda driver: EC.element_to_be_clickable(driver.find_element_by_xpath(self.account_menu))
        )

    def get_account_menu_classes(self):
        self.driver.find_element_by_xpath(self.account_menu).get_atrribute("class").split()

    def get_username_from_account_menu(self):
        return WebDriverWait(self.driver, 10).until(
            lambda driver: driver.find_element_by_xpath(self.account_menu_username).text
        )

    def get_email_from_account_menu(self):
        return WebDriverWait(self.driver, 10).until(
            lambda driver: driver.find_element_by_xpath(self.account_menu_email).text
        )

    def add_second_email(self):
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, self.account_menu_add_email))
        )
        self.driver.find_element_by_xpath(self.account_menu_add_email).click()
        WebDriverWait(self.driver, 10).until(
            lambda driver: EC.element_to_be_clickable(driver.find_element_by_xpath(self.LOGIN_POPUP))
        )

    def is_both_emails_present(self):
        is_first_block_present = WebDriverWait(self.driver, 10).until(
            lambda driver: driver.find_element_by_xpath(self.account_menu_first_email_block).is_displayed()
        )
        is_second_block_present = WebDriverWait(self.driver, 10).until(
            lambda driver: driver.find_element_by_xpath(self.account_menu_second_email_block).is_displayed()
        )
        if is_first_block_present and is_second_block_present:
            return True
        else:
            return False


class MailboxForm(Form):
    EMAIL_REF = '//*[@id="js-mailbox-user"]'
    EMAIL_DROPDOWN = '//*[@id="multiAuthMenuDropdown"]/div'
    ADD_EMAIL_FORM = '//div[@class="multiauth__menu__dropdown__login"]'
    ADD_EMAIL_BUTTON = '//a[@class="multiauth__menu__dropdown__login__link js-login"]'
    PRELOADER = '//*[@class="x-ph__popup__content__preloader"]'
    MAILBOX_PRELOADER = '//*[@class="multiauth__menu__dropdown__loader"]'
    LOGIN_FORM = '//*[@id="x-ph__authForm"]/div'

    def get_user_email(self):
        return WebDriverWait(self.driver, 10).until(
            lambda driver: driver.find_element_by_xpath(self.EMAIL_REF).text
        )

    def open_email_dropdown(self):
        WebDriverWait(self.driver, 10).until(
            lambda driver: EC.element_to_be_clickable(driver.find_element_by_xpath(self.EMAIL_REF))
        )
        self.driver.find_element_by_xpath(self.EMAIL_REF).click()
        WebDriverWait(self.driver, 10).until(
            lambda driver: EC.element_to_be_clickable(driver.find_element_by_xpath(self.EMAIL_DROPDOWN))
        )

    def add_new_email(self):
        WebDriverWait(self.driver, 10).until(
            lambda driver: EC.invisibility_of_element_located(driver.find_element_by_xpath(self.MAILBOX_PRELOADER))
        )
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, self.ADD_EMAIL_BUTTON))
        )
        self.driver.find_element_by_xpath(self.ADD_EMAIL_BUTTON).click()
        WebDriverWait(self.driver, 10).until(
            lambda driver: EC.invisibility_of_element_located(driver.find_element_by_xpath(self.PRELOADER))
        )
        WebDriverWait(self.driver, 10).until(
            lambda driver: EC.element_to_be_clickable(driver.find_element_by_xpath(self.LOGIN_FORM))
        )

    def is_both_emails_present(self):
        first_email_block = '//*[@id="multiAuthMenuList"]/div[1]'
        second_email_block = '//*[@id="multiAuthMenuList"]/div[2]'
        if self.is_element_present(first_email_block) and self.is_element_present(second_email_block):
            return True
        else:
            return False
