*** Settings ***
Library     httpbin_library.HttpbinLibrary
Resource    ../res/status_codes.robot


*** Test Cases ***
Not contain headers
    [Template]    GET request should not contain headers
    @{EMPTY}
    test-header
    Hello    My-test-name
    h1    h2    h3    h4    h5    h6    h7

Contain headers
    [Template]    GET request should contain headers
    &{EMPTY}
    test-header=Some Data
    Hello=World    My-test-name=Contain headers
    h1=1    h2=2    h3=3    h4=4    h5=5    h6=6    h7=7
    # todo: move to separate file or variable
    Some-long-long-long-long-long-long-long-long-long-long-long-long-long-long-long-long-long-long-long-long-long-long-long-long-long-long-long-long-long-long-header=Some long long long long long long long long long long long long long long long long long long long long long long long long long long long long long long long long long long long long long long long long long long long long long value

Default headers
    [Template]    GET request should contain default headers
    Host=httpbin.org    User-Agent=python-requests/2.18.4
    # Not very smart: the sample below just checks implementation of HttpbinLibrary (not service http://httpbin.org/ at all)
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
