*** Settings ***
Library     httpbin_library.HttpbinLibrary
Resource    ../res/status_codes.robot


*** Test Cases ***
Successful authentication
    [Template]    Authentication ${user}/${password} should success
    # Not empty username and password
    ${VALID_USERNAME}    ${VALID_PASSWORD}
    ${VALID_USERNAME}    ${VALID_USERNAME}
    ${VALID_PASSWORD}    ${VALID_PASSWORD}

    # Allowed characters in username and password
    ${USERNAME_CHARACTERS}    ${VALID_PASSWORD}
    ${VALID_USERNAME}    ${PASSWORD_CHARACTERS}
    ${USERNAME_CHARACTERS}    ${PASSWORD_CHARACTERS}

Failed authentication
    [Template]    Authentication ${correct_user}/${correct_password} as ${entered_user}/${entered_password} should fail
    # Invalid username
    ${VALID_USERNAME}    ${VALID_PASSWORD}    ${INVALID_USERNAME}    ${VALID_PASSWORD}
    # Invalid password
    ${VALID_USERNAME}    ${VALID_PASSWORD}    ${VALID_USERNAME}    ${INVALID_PASSWORD}
    # Invalid username and password
    ${VALID_USERNAME}    ${VALID_PASSWORD}    ${INVALID_USERNAME}    ${INVALID_PASSWORD}

Invalid authentication request
    [Template]    Authentication ${user}/${password} should fail
    # Empty username
    ${EMPTY}    ${VALID_PASSWORD}
    # Empty password
    ${VALID_USERNAME}    ${EMPTY}
    # Empty username and password
    ${EMPTY}    ${EMPTY}


*** Keywords ***
Authentication ${user}/${password} should success
    When authenticate ${user}/${password} as ${user}/${password}
    Then status code should be    ${OK}
    and user ${user} should be authenticated

Authentication ${user:[^/]*}/${password:[^/]*} should fail
    When authenticate ${user}/${password} as ${user}/${password}
    Then status code should be    ${NOT FOUND}

Authentication ${correct_user}/${correct_password} as ${entered_user}/${entered_password} should fail
    When authenticate ${correct_user}/${correct_password} as ${entered_user}/${entered_password}
    Then status code should be    ${UNAUTHORIZED}


*** Variables ***
# Valid and invalid usernames and passwords
${VALID_USERNAME}    Andrew
${INVALID_USERNAME}    andreV
${VALID_PASSWORD}    5eCRe7
${INVALID_PASSWORD}    SecreT

# Allowed characters in username and password
# Attention: username can not contain a colon sign (:), but password can.
${USERNAME_CHARACTERS}    !@\#$^&*()_+-=,.<>?;'"[]{}\\|${SPACE}
${PASSWORD_CHARACTERS}    !@\#$^&*()_+-=,.<>?;:'"[]{}\\|${SPACE}
