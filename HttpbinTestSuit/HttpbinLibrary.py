# todo: add tags

# todo? rename module to httpbin_library.py
# todo? add documentation to robot framework files

# todo: name columns where applicable
"""Robot Framework library for testing http://httpbin.org/.

Endpoints to test:
    http://httpbin.org/basic-auth/:user/:passwd
    http://httpbin.org/get
    http://httpbin.org/stream/:n
"""

import requests
from robot.api.deco import keyword
from robot.api import logger


class HttpbinLibrary:
    """Main (and the only) class of the library."""

    _BASE_URL = 'http://httpbin.org/'

    def __init__(self):
        """Initialize self."""
        self._response = None

    def _log_response(self):
        if self._response is not None:
            logger.info('Status code: ' + str(self._response.status_code))
            logger.debug('Headers:\n' + str(self._response.headers))
            logger.info('Response body:\n' + self._response.text)
            logger.debug('Hexadecimal response body:\n'
                         + self._response.content.hex())
        else:
            logger.warn('Response is None')

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
        self._response = requests.get(
            self._BASE_URL + 'basic-auth/{}/{}'.format(
                requests.utils.quote(correct_user),
                requests.utils.quote(correct_password)
            ),
            auth=(entered_user, entered_password),
        )
        self._log_response()

    @keyword('Send GET request with headers')
    def get(self, headers=None):
        """Send GET request and receive GET data in response body.

        :param headers: headers to be added to request
        :type headers: Dict[str, str]
        :rtype: None
        """
        self._response = requests.get(self._BASE_URL + 'get', headers=headers)
        self._log_response()

    @keyword('Get stream of ${n} lines')
    def stream(self, n):
        """Send GET request and receive min(n, 100) lines in response
        body.

        :param n: number of lines to receive in response body
        :type n: int
        :rtype: None
        """
        self._response = requests.get(self._BASE_URL + 'stream/{}'.format(n))
        self._log_response()

    def status_code_should_be(self, expected_status_code):
        """Check if response status code is as expected.

        Should invoke one of the following methods first:
            HttpbinLibrary.basic_auth,
            HttpbinLibrary.get,
            HttpbinLibrary.stream.

        :type expected_status_code: int
        :rtype: None
        """
        if str(self._response.status_code) != str(expected_status_code):
            raise AssertionError(
                "Status code should be '{}', but '{}' received.".format(
                    expected_status_code,
                    self._response.status_code,
                )
            )

    @keyword('User ${username} should be authenticated')
    def check_authentication(self, username):
        """Check if user is authenticated with correct username.

        Should invoke HttpbinLibrary.basic_auth first.

        :param username: correct authentication username
        :type username: int
        :rtype: None
        """
        json_response = self._response.json()
        if 'authenticated' not in json_response:
            raise AssertionError(
                "Response body does not contain 'authenticated' key.")
        if json_response['authenticated'] is not True:
            raise AssertionError('User is not authenticated.')
        if 'user' not in json_response:
            raise AssertionError("Response body does not contain 'user' key.")
        if json_response['user'] != username:
            raise AssertionError(
                "Username should be '{}', but '{}' received.".format(
                    username,
                    json_response['user'],
                )
            )

    def response_body_should_contain_headers(self, headers):
        """Check if response body contain specified headers.

        Should invoke HttpbinLibrary.get first.

        :param headers: headers to be in response body
        :type headers: Dict[str, str]
        :rtype: None
        """
        json_response = self._response.json()
        if 'headers' not in json_response:
            raise AssertionError(
                "Response body does not contain 'headers' key.")
        for name, value in headers.items():
            titled = name.title()
            if titled not in json_response['headers']:
                raise AssertionError(
                    "Response body does not contain '{}' header.".format(
                        titled)
                )
            if json_response['headers'][titled] != value:
                raise AssertionError(
                    "Header '{}' should contain '{}', but '{}'"
                    " received.".format(titled, value, json_response[titled],)
                )

    def response_body_should_not_contain_headers(self, headers_names):
        """Check if response body not contain specified headers.

        Should invoke HttpbinLibrary.get first.

        :param headers_names: headers to not be in response body
        :type headers_names: List[str]
        :rtype: None
        """
        json_response = self._response.json()
        if 'headers' not in json_response:
            raise AssertionError(
                "Response body does not contain 'headers' key.")
        for name in headers_names:
            titled = name.title()
            if titled in json_response['headers']:
                raise AssertionError("Response body contains '{}' header,"
                                     " but should not.".format(titled))

    def number_of_lines_should_be(self, expected_number_of_lines):
        """Check if number of lines in response body is as expected.

        Should invoke HttpbinLibrary.stream first.

        :type expected_number_of_lines: int
        :rtype: None
        """
        actual_number_of_lines = self._response.text.count('\n')
        if actual_number_of_lines != int(expected_number_of_lines):
            raise AssertionError(
                "Number of lines should be '{}', but '{}' received.".format(
                    expected_number_of_lines,
                    actual_number_of_lines,
                )
            )
