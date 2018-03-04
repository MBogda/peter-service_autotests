*** Settings ***
Library      httpbin_library.HttpbinLibrary
Resource     ../res/status_codes.robot
Variables    ../res/headers.py


*** Test Cases ***
Not contain headers
    :FOR    ${headers}    in    @{HEADERS_LIST}
    \    GET request should not contain headers    @{headers}

Contain headers
    :FOR    ${headers}    in    @{HEADERS_LIST}
    \    GET request should contain headers    &{headers}

Default headers
    [Template]    GET request should contain default headers
    Host=httpbin.org    User-Agent=python-requests/2.18.4
    # Not very smart: the sample below just checks implementation of
    # HttpbinLibrary (not service http://httpbin.org/ at all)
    hOsT=httpbin.org    uSeR-aGeNt=python-requests/2.18.4


*** Keywords ***
GET request should contain headers
    [Arguments]    &{headers}
    When send GET request with headers    ${headers}
    Then status code should be    ${OK}
    and response body should contain headers    ${headers}

GET request should not contain headers
    [Arguments]    @{headers_names}
    When send GET request with headers
    Then status code should be    ${OK}
    and response body should not contain headers    ${headers_names}

GET request should contain default headers
    [Arguments]    &{headers}
    When send GET request with headers
    Then status code should be    ${OK}
    and response body should contain headers    ${headers}
