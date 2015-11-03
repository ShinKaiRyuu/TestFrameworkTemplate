from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from webium import Find, Finds

from .base_page import BasePage


class MainPage(BasePage):
    url_path = '/'

    header_links = Finds(by=By.XPATH, value='//ul[@data-ng-if="baseCtrl.authSrv.isLoggedIn()"]/li/a')

    def get_headers_links(self):
        return self.header_links
