from sys import platform
from webium.driver import get_driver
from helpers.app_helpers import get_requests_app_cookies


def get_updated_driver():
    driver = get_driver()
    driver.set_page_load_timeout(60)
    if 'linux' in platform:
        driver.set_window_position(0, 0)
        driver.set_window_size(1366, 768)
    else:
        driver.maximize_window()
    return driver


def update_driver_cookies(driver, credentials):
    r_cookies = get_requests_app_cookies(credentials)
    driver.delete_all_cookies()
    for c in r_cookies:
        driver.add_cookie({'name': c.name, 'value': c.value, 'domain': c.domain})