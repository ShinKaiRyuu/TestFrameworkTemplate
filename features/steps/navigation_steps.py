from behave import *
from nose.tools import assert_in
import time
from webium.driver import get_driver

import pages

use_step_matcher("re")

PAGES_MAP = {
    'Main': pages.MainPage,
    'Login': pages.LoginPage,
}


@when("I open (?P<page_name>.+) page")
@step("I am on (?P<page_name>.+) page")
def step_impl(context, page_name):
    context.page_name = page_name
    page = PAGES_MAP[page_name]
    context.page = page(url=''.join([context.app_url, page.url_path]))
    context.page.open()



@then("I want to see '(?P<page_name>.+)' page")
def step_impl(context, page_name):
    context.page.wait_for_loading()
    page = PAGES_MAP[page_name]
    context.page = page()

    if hasattr(context.page, 'default_wait'):
        context.page.default_wait()

    assert_in(page.url_path, get_driver().current_url)
