# todo: add logging

# todo? rename module to httpbin_library.py
# todo? robot framework documentation
# todo: why not continue testing after fail in Template test case?
"""Robot Framework library for testing http://httpbin.org/.

Endpoints to test:
    http://httpbin.org/basic-auth/:user/:passwd
    http://httpbin.org/get
    http://httpbin.org/stream/:n
"""

import requests
from robot.api.deco import keyword

class HttpbinLibrary:
    """Main (and the only) class of the library."""

    _BASE_URL = 'http://httpbin.org/'

    def __init__(self):
        """Initialize self."""
        self._response = None

    @keyword('Authenticate ${correct_user}/${correct_password}'
             ' as ${entered_user}/${entered_password}')
    def basic_auth(self, correct_user, correct_password,
                   entered_user, entered_password):
        """Send GET request that require HTTP Basic authentication.

        :param correct_user: username sent via URL (i.e. "correct"
            username)
        :type correct_user: str
        :param correct_password: password sent via URL (i.e. "correct"
            password)
        :type correct_password: str
        :param entered_user: username sent via HTTP Basic authentication
            (i.e. "entered" username)
        :type entered_user: str
        :param entered_password: password sent via HTTP Basic
            authentication (i.e. "entered" password)
        :type entered_password: str
        :rtype: None
        """
        print(correct_user, correct_password, sep='::')
        print(entered_user, entered_password, sep='::')
        self._response = requests.get(
            self._BASE_URL + 'basic-auth/{}/{}'.format(
                requests.utils.quote(correct_user),
                requests.utils.quote(correct_password)
            ),
            auth=(entered_user, entered_password),
        )

    @keyword('Send GET request with headers')
    def get(self, **headers):
        """Send GET request and receive GET data in response body.

        :param headers: headers to be added to request
        :type headers: Dict[str, str]
        :rtype: None
        """
        self._response = requests.get(self._BASE_URL + 'get', headers=headers)

    @keyword('Get stream of ${n} lines')
    def stream(self, n):
        """Send GET request and receive min(n, 100) lines in response
        body.

        :param n: number of lines to receive in response body
        :type n: int
        :rtype: None
        """
        self._response = requests.get(self._BASE_URL + 'stream/{}'.format(n))

    def status_code_should_be(self, expected_status_code):
        """Check if response status code is as expected.

        Should invoke one of the following methods first:
            basic_auth,
            get,
            stream.

        :type expected_status_code: int
        :rtype: None
        """
        assert str(self._response.status_code) == str(expected_status_code), \
            'Status code should be {} but was {}.'.format(
                expected_status_code,
                self._response.status_code,
            )

    @keyword('User ${username} should be authenticated')
    def check_authentication(self, username):
        """Check if user is authenticated with correct username.

        Should invoke method basic_auth first.

        :param username: correct authentication username
        :type username: int
        :rtype: None
        """
        assert self._response.json()['authenticated'] is True, \
            'User is not authenticated'
        assert self._response.json()['user'] == username, \
            'Username should be {} but was {}'.format(
                username,
                self._response.json()['user'],
            )

    def response_body_should_contain_headers(self, **headers):
        """Check if response body contain specified headers.

        Should invoke method get first.

        :param headers: headers to be in response body
        :type headers: Dict[str, str]
        :rtype: None
        """
        # print(headers.items())
        # print(self._response.text)
        for name, value in headers.items():
            # print(name, value)
            assert self._response.json()['headers'][name.title()] == value

    def response_body_should_not_contain_headers(self, *headers_names):
        """Check if response body not contain specified headers.

        Should invoke method get first.

        :param headers_names: headers to not be in response body
        :type headers_names: List[str]
        :rtype: None
        """
        print(headers_names)
        for name in headers_names:
            assert name.title() not in self._response.json()['headers']

    def number_of_lines_should_be(self, expected_number_of_lines):
        """Check if number of lines in response body is as expected.

        Should invoke method stream first.

        :type expected_number_of_lines: int
        :rtype: None
        """
        actual_number_of_lines = self._response.text.count('\n')
        assert actual_number_of_lines == int(expected_number_of_lines), \
            'Number of lines should be {} but was {}'.format(
                expected_number_of_lines,
                actual_number_of_lines,
            )
