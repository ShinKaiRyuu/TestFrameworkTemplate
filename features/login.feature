Feature: Log in

  Scenario: Successful login
    Given I am on Main page
    When I click on login link
    Then I want to see 'Login' page
    When I login with username 'your@username.here' and password 'your.password'
    Then I want to see 'Main' page
    And I want to see that I am logged in
    When I click on Logout button
    Then I want to see that I am logged out

  Scenario: Unsuccessful login
    Given I am on Login page
    When I login with username 'abcd@ed.ba' and password '111111'
    Then I want to see error message "Incorrect username or password."
