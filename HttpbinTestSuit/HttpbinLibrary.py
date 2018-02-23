# todo? other way to create url-s
# todo: add logging
# todo: add documentation
# todo? robot framework documentation?
# todo: why not continue testing after fail in Template test case?
import requests

from robot.api.deco import keyword


class HttpbinLibrary:
    _base_url = 'http://httpbin.org/'
    _response = None

    @keyword('Authenticate ${url_user}/${url_password} as ${auth_user}/${auth_password}')
    def basic_auth(self, url_user, url_password, auth_user, auth_password):
        print(url_user, url_password, sep='::')
        self._response = requests.get(
            # todo: diff
            self._base_url + 'basic-auth/{}/{}'.format(requests.utils.quote(url_user), requests.utils.quote(url_password)),
            # self._base_url + 'basic-auth/{}/{}'.format(url_user, url_password),
            auth=(auth_user, auth_password)
        )

    @keyword('Send GET request with headers')
    def get(self, **headers):
        self._response = requests.get(self._base_url + 'get', headers=headers)

    @keyword('Get stream of ${n} lines')
    def stream(self, n):
        self._response = requests.get(self._base_url + 'stream/{}'.format(n))

    def status_code_should_be(self, expected_status_code):
        assert str(self._response.status_code) == str(expected_status_code), \
            'Status code should be {} but was {}.'.format(expected_status_code, self._response.status_code)

    @keyword('User ${user} should be authenticated')
    def check_authentication(self, user):
        assert self._response.json()['authenticated'] is True, \
            'User is not authenticated'
        assert self._response.json()['user'] == user, \
            'Username should be {} but was {}'.format(user, self._response.json()['user'])

    def response_should_contain_headers(self, **headers):
        # print(headers.items())
        # print(self._response.headers)
        for name, value in headers.items():
            # print(name, value)
            # assert self._response.headers[name] == value
            assert self._response.json()['headers'][name] == value

    def response_should_not_contain_headers(self, **headers):
        # print(headers.items())
        for name, value in headers.items():
            # assert name not in self._response.headers
            assert name not in self._response.json()['headers']

    def number_of_lines_should_be(self, expected_number_of_lines):
        actual_number_of_lines = self._response.text.count('\n')
        assert actual_number_of_lines == int(expected_number_of_lines), \
            'Number of lines should be {} but was {}'.format(expected_number_of_lines, actual_number_of_lines)

    # def trying(self, **kwargs):
    #     print(kwargs)
