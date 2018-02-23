*** Settings ***
Library    HttpbinLibrary.py


*** Test Cases ***
Successful authentication
    [Template]    Authentication ${user}/${password} should success
    Andrew    5eCRe7
    Andrew    Andrew
    # allowed characters in username and password
    !@#$^&*()_+-=,.<>?;'"[]{}\|${SPACE}    password
    username    !@#$^&*()_+-=,.<>?;:'"[]{}\|${SPACE}
                # !@#$%^&*()_+-=.,<>/?;:'"[]{}\|

Failed authentication
    [Template]    Authentication ${url_user}/${url_password} as ${auth_user}/${auth_password} should fail
    # Invalid username
    Andrew    5eCRe7    Andrev    5eCRe7
    # Invalid password
    Andrew    5eCRe7    Andrew    5eCReT
    # Invalid username and password
    Andrew    5eCRe7    andrew    seCRe7

Invalid authentication request
# todo? more tests
    [Template]    Authentication ${user}/${password} should fail
    # Empty username
    ${EMPTY}    5eCRe7
    # Empty password
    Andrew    ${EMPTY}
    # Empty username and password
    ${EMPTY}    ${EMPTY}
    # Andrew    :/?#[]@
    # Andrew    :?#[]@%

*** Keywords ***
Authentication ${user}/${password} should success
    When authenticate ${user}/${password} as ${user}/${password}
    Then status code should be    ${OK}
    and user ${user} should be authenticated

Authentication ${user:[^/]*}/${password:[^/]*} should fail
    When authenticate ${user}/${password} as ${user}/${password}
    Then status code should be    ${NOT FOUND}

Authentication ${url_user}/${url_password} as ${auth_user}/${auth_password} should fail
    When authenticate ${url_user}/${url_password} as ${auth_user}/${auth_password}
    Then status code should be    ${UNAUTHORIZED}


*** Variables ***
${OK}    200
${UNAUTHORIZED}    401
${NOT FOUND}    404
