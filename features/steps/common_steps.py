import time
from behave import *
from selenium.common.exceptions import NoSuchElementException
from webium.driver import get_driver
from helpers.files import get_full_path
from nose.tools import assert_true, assert_equal, assert_not_in, assert_in, assert_is_none
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

use_step_matcher("re")

types_map = {
    'link': 'link',
    'sort': 'sort',
    'button': 'btn',
    'popup': 'popup',
    'dropdown': 'dd',
    'list': 'list',
    'input': 'input',
    'tooltip': 'tooltip',
    'text': 'text',
}

properties_map = {
    'disabled': 'true',
}

expected_conditions_map = {
    'present': EC.presence_of_element_located,
    'clickable': EC.element_to_be_clickable,
    'visible': EC.visibility_of_element_located,
    'invisible': EC.invisibility_of_element_located,
}


def get_element(context, element_name, element_type):
    return getattr(context.page, '_'.join([element_name.lower().replace(' ', '_'), types_map[element_type]]))


@step("I hover on (?P<element_name>.+) (?P<element_type>.+)")
def hover_element(context, element_name, element_type):
    element = get_element(context, element_name, element_type)
    context.page.hover(element)


@step("I click on (?P<element_name>.+) (?P<element_type>.+)")
def click_element(context, element_name, element_type):
    get_element(context, element_name, element_type).click()
    context.page.wait_for_loading()
    context.page.wait_for_loader_disappear()


@when("I fill (?P<element_name>.+) (?P<element_type>.+) with text: (?P<text>.+)")
def send_keys_to_element(context, element_name, element_type, text):
    get_element(context, element_name, element_type).send_keys(text)


@step('I set file with name: (?P<file_name>.+) to upload into: (?P<element_name>.+) (?P<element_type>.+)')
def set_file_to_upload(context, file_name, element_name, element_type):
    send_keys_to_element(context, element_name, element_type, get_full_path(file_name))


@step('I wait for (?P<element_name>.+) (?P<element_type>.+) is (?P<condition>.+)')
def wait_for_element(context, element_name, element_type, condition):
    wait = WebDriverWait(context.driver, 25)
    wait.until(expected_conditions_map[condition]((By.XPATH, get_element(context, element_name, element_type))))


@step("I assert that (?P<element_name>.+) (?P<element_type>.+) is (?P<property>.+)")
def assert_element_has_property(context, element_name, element_type, property):
    assert_equal(get_element(context, element_name, element_type).get_attribute(property), properties_map[property])


@when("I select (?P<element_text>.+) from (?P<element_name>.+) list")
def select_element_from_list(context, element_text, element_name):
    list_of_elements = get_element(context, element_name, 'list')
    list_of_elements_text = [x.text.strip() for x in list_of_elements]
    assert_in(element_text, list_of_elements_text)
    list_of_elements[list_of_elements_text.index(element_text)].click()


@then("There is no (?P<element_text>.+) in (?P<element_name>.+) list")
def assert_element_not_in_list(context, element_text, element_name):
    list_of_elements = get_element(context, element_name, 'list')
    list_of_element_text = [x.text.strip() for x in list_of_elements]
    assert_not_in(element_text, list_of_element_text)


@then("There is no (?P<element_name>.+) (?P<element_type>.+) on page")
def assert_element_not_in_list(context, element_name, element_type):
    element = None
    try:
        element = get_element(context, element_name, element_type)
    except NoSuchElementException:
        pass
    finally:
        assert_is_none(element)


@then("I want (?P<element_name>.+) (?P<element_type>.+) text is: (?P<expected_text>.+)")
def assert_element_text_is(context, element_name, element_type, expected_text):
    assert_equal(
        get_element(context, element_name, element_type)[0].text
        if isinstance(get_element(context, element_name, element_type), list)
        else get_element(context, element_name, element_type).text, expected_text)


@then("I want to get result - (?P<result>.+)")
def step_impl(context, result):
    context.execute_steps("""
        Then {}
    """.format(result))


@step("I want to see table with data")
def step_impl(context):
    datas = context.page.get_data()
    assert_true(len(datas) >= 1)


@step("I reloading page")
def reload_page(context):
    context.driver.refresh()
    context.page.wait_for_loading(240)


@step("deleted cookies")
def step_impl(context):
    get_driver().delete_all_cookies()


@step('fail')
@step('Fail')
def step_impl(context):
    raise NotImplementedError


@when("I clear (?P<element_name>.+) (?P<element_type>.+)")
def clear_field(context, element_name, element_type):
    get_element(context, element_name, element_type).clear()
    time.sleep(2)


@step("I wait for page is load")
def wait_for_page_loading(context):
    context.page.wait_for_loading()
    context.page.wait_for_loader_disappear()
