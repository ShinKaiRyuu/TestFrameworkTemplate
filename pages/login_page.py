import time
from selenium.webdriver.common.by import By
from webium import Find, Finds
from .base_page import BasePage


class LoginPage(BasePage):
    url_path = '/login'

    username = Find(value='#login_field')
    password = Find(value='#password')
    sign_in_btn = Find(by=By.XPATH, value='//input[@name="commit"]')
    error_message = "#js-flash-container"


    def login_with(self, credentials):
        self.clear_send_keys('username', credentials)
        self.clear_send_keys('password', credentials)
        self.sign_in_btn.click()
        self.wait_for_loading()

    def get_error_messages(self):
        time.sleep(1)
        errors = Finds(value=self.error_message, context=self)
        return [e.text for e in errors if e.text]