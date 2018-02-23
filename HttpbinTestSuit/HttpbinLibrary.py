# todo: add logging
# todo: add documentation

# todo? rename module to httpbin_library.py
# todo? robot framework documentation
# todo: why not continue testing after fail in Template test case?
"""docstring here"""

import requests
from robot.api.deco import keyword


class HttpbinLibrary:
    _BASE_URL = 'http://httpbin.org/'
    _response = None

    @keyword('Authenticate ${url_user}/${url_password}'
             ' as ${auth_user}/${auth_password}')
    def basic_auth(self, url_user, url_password, auth_user, auth_password):
        # print(url_user, url_password, sep='::')
        self._response = requests.get(
            self._BASE_URL + 'basic-auth/{}/{}'.format(
                requests.utils.quote(url_user),
                requests.utils.quote(url_password)
            ),
            # todo something with that string:
            # self._BASE_URL + 'basic-auth/{}/{}'.format(url_user, url_password),
            auth=(auth_user, auth_password),
        )

    @keyword('Send GET request with headers')
    def get(self, **headers):
        self._response = requests.get(self._BASE_URL + 'get', headers=headers)

    @keyword('Get stream of ${n} lines')
    def stream(self, n):
        self._response = requests.get(self._BASE_URL + 'stream/{}'.format(n))

    def status_code_should_be(self, expected_status_code):
        assert str(self._response.status_code) == str(expected_status_code), \
            'Status code should be {} but was {}.'.format(
                expected_status_code,
                self._response.status_code,
            )

    @keyword('User ${user} should be authenticated')
    def check_authentication(self, user):
        assert self._response.json()['authenticated'] is True, \
            'User is not authenticated'
        assert self._response.json()['user'] == user, \
            'Username should be {} but was {}'.format(
                user,
                self._response.json()['user'],
            )

    def response_body_should_contain_headers(self, **headers):
        # print(headers.items())
        # print(self._response.text)
        for name, value in headers.items():
            # print(name, value)
            assert self._response.json()['headers'][name.title()] == value

    def response_body_should_not_contain_headers(self, *headers_names):
        print(headers_names)
        for name in headers_names:
            assert name.title() not in self._response.json()['headers']

    def number_of_lines_should_be(self, expected_number_of_lines):
        actual_number_of_lines = self._response.text.count('\n')
        assert actual_number_of_lines == int(expected_number_of_lines), \
            'Number of lines should be {} but was {}'.format(
                expected_number_of_lines,
                actual_number_of_lines,
            )
