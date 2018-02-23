# todo: right syntax for keywords?
*** Settings ***
Library    HttpbinLibrary.py


*** Test Cases ***
Contain headers
# todo: headers naming
    [Template]    GET response should contain headers
    &{EMPTY}
    olol=kuku
    privet=olol    kuku=hello
    h1=1    h2=2    h3=3    h4=4    h5=5    h6=6    h7=7

Not contain headers
    [Template]    GET response should not contain headers
    &{EMPTY}
    olol=kuku
    privet=olol    kuku=hello
    h1=1    h2=2    h3=3    h4=4    h5=5    h6=6    h7=7

Default headers
    GET response should contain default headers    Host=httpbin.org    User-Agent=python-requests/2.18.4


*** Keywords ***
# todo: maybe rename response to request?
GET response should contain headers
    [Arguments]    &{headers}
    When send GET request with headers    &{headers}
    Then status code should be    ${OK}
    and response should contain headers    &{headers}

GET response should not contain headers
    [Arguments]    &{headers}
    When send GET request with headers
    Then status code should be    ${OK}
    and response should not contain headers    &{headers}

GET response should contain default headers
    [Arguments]    &{headers}
    When send GET request with headers
    Then status code should be    ${OK}
    and response should contain headers    &{headers}


*** Variables ***
${OK}    200
