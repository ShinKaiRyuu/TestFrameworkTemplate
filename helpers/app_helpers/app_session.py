import re
from bs4 import BeautifulSoup
from nose.tools import assert_equal, assert_in, assert_true
import pages

import requests

APP_URL = 'https://www.github.com'
ADMIN_CREDENTIALS = {'username': 'admin@example.com', 'password': 'pk$321'}
ROOT_CREDENTIALS = {'username': 'root', 'password': '123456'}
API_URLS_MAP = {
    'login': '/api/login',
    'logout': '/api/logout'
}

_admin_session = None


def get_requests_app_cookies(credentials):
    s = _get_logged_session(credentials)
    return s.cookies


def get_url(url_path, app_url=APP_URL):
    return ''.join([app_url, url_path])


def _get_logged_session(credentials):
    url = get_url(API_URLS_MAP['login'])
    s = requests.Session()
    payload = {
        'email': credentials['username'],
        'password': credentials['password']
    }
    r = s.post(url, data=payload, verify=False)
    assert_equal(r.status_code, 200)
    assert_true(r.json()['data']['isAuthenticated'])
    return s


def get_csrf_token(response, on_form=False):
    response_content = response.text
    csrf_pattern = re.compile('<meta name="csrf-token" content="(.*?)">')
    if on_form:
        csrf_pattern = re.compile("<input type='hidden' name='csrfmiddlewaretoken' value='(.*?)'")
    return csrf_pattern.findall(response_content)[0]


def _get_data_key(source_name, payload, response):
    name_key_source_map = {
        'page': '[name]',
        'partner': '[name]',
        'product': '[title]',
    }
    key_part = name_key_source_map[source_name]
    name = payload[[k for k in payload.keys() if key_part in k][0]]
    soup = BeautifulSoup(response.text)
    trs = soup.findAll(lambda tag: tag.name == 'tr' and 'data-key' in tag.attrs)
    tr = [tr for tr in trs if name in tr.text][0]
    return tr['data-key']
