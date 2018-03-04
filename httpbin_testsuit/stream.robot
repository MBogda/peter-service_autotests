*** Settings ***
Library     httpbin_library.HttpbinLibrary
Resource    ../res/status_codes.robot


*** Test Cases ***
Valid stream
    [Template]    Stream of ${request_n} lines should be valid and have ${expected_n} lines
    0             0
    5             5
    67            67
    99            99
    100           100
    101           100
    120           100
    2000000000    100

Invalid stream
    [Template]    Stream of ${request_n} lines should be invalid
    -7
    3.14
    x
    nnn
    ?n=5
    ${EMPTY}


*** Keywords ***
Stream of ${request_n} lines should be valid and have ${expected_n} lines
    When get stream of ${request_n} lines
    Then status code should be    ${OK}
    and number of lines should be    ${expected_n}

Stream of ${request_n} lines should be invalid
    When get stream of ${request_n} lines
    Then status code should be    ${NOT FOUND}
