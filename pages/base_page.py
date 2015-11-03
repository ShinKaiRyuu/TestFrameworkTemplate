from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from webium import BasePage as WebiumBasePage, Find


class BasePage(WebiumBasePage):
    url_path = None

    a_tag = "//a[contains(.,'{link_text}')]"
    login_link = Find(by=By.XPATH, value=a_tag.format(link_text='Sign in'))
    logout_btn = Find(by=By.XPATH, value="//button[contains(.,'Sign out')]")
    account_options_btn = Find(by=By.XPATH, value=a_tag.replace('.', '@aria-label').format(link_text='View profile and more'))

    loader_xpath = "//div[@id='prestatus']"

    def clear_send_keys(self, element_name, kwargs):
        value = kwargs.get(element_name)
        element = getattr(self, element_name)
        element.clear()
        element.send_keys(value)

    def hover(self, element):
        hov = ActionChains(self._driver).move_to_element(element)
        hov.perform()
        self.wait_for_loading()
        self.wait_for_loader_disappear()

    def get_login_status(self):
        try:
            self.account_options_btn.click()
            return 'logged in' if self.logout_btn.is_displayed() == True else 'logged out'
        except NoSuchElementException:
            return 'logged out'

    def wait_for_loading(self, seconds=180):
        wait = WebDriverWait(self._driver, seconds)
        wait.until(lambda x: self._driver.execute_script('return jQuery.active == 0') is True)

    def replace_bad_elements(self, css_locator):
        self._driver.execute_script("$('{}').remove()".format(css_locator))

    def is_loader_displayed(self, *args):
        return self._driver.find_element_by_xpath(self.loader_xpath).is_displayed()

    def wait_for_loader_disappear(self):
        WebDriverWait(self._driver, timeout=500).until_not(
            self.is_loader_displayed, "Timeout waiting for loader disappear")
