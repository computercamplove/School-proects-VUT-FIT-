Feature: Check visibility of published intems

Scenario Outline: 1. Make pages not published by Admin 
    Given <Page> with user "admin" logged in
    And "state" is "Satte: Published" 
    And "state"'s name is "blue"
    When Admin click "State: Published"
    And click "Send back"
    Then "state" become "State: Private"
    And appears "info Item state changed." message
    And color "state"'s name changes to "red"

    Examples:
        | Page           |
        | Home           |
        | Methods        |
        | Tools          |
        | Use Cases      |
        | Organizations  |
        | Users          |


Scenario Outline: 2. Check visibility of pages by Itsreviewer when Admin make it not published
    Given Page "Home" with user "itsreviewer" logged in
    Then <Page> does not appear on "navigation bar"
    And page "Home" has message "Insufficient Privileges"

    Examples:
        | Page           |
        | Methods        |
        | Tools          |
        | Use Cases      |
        | Organizations  |
        | Users          |


Scenario Outline: 3. Send pages to review by Admin
    Given <Page> with user "admin" logged in
    And "state" is "Satte: Private" 
    And "state"'s name is "red"
    When Admin click "State: Private"
    And click "Submit for publication"
    Then "state" become "State: Pending review"
    And appears "info Item state changed." message
    And color "state"'s name changes to "green"

    Examples:
        | Page           |
        | Home           |
        | Methods        |
        | Tools          |
        | Use Cases      |
        | Organizations  |
        | Users          |


Scenario Outline: 4. Retract pages by Admin
    Given <Page> with user "admin" logged in
    And "state" is "Satte: Pending review" 
    And "state"'s name is "green"
    When Admin click "State: Pending review"
    And click "Retract"
    Then "state" become "State: Private"
    And appears "info Item state changed." message
    And color "state"'s name changes to "red"

    Examples:
        | Page           |
        | Home           |
        | Methods        |
        | Tools          |
        | Use Cases      |
        | Organizations  |
        | Users          |

Scenario Outline: 5. itsreviewer sends back pages from review by admin
    Given <Page> with user "itsreviewer" logged in
    And "state" is "Satte: Pending review" 
    And "state"'s name is "green"
    When Admin click "Satte: Pending review"
    And click "Send back"
    Then <Page> does not appear on "navigation bar"
    And user "itsreviewer" on "Home" Page
    And appears "info Item state changed." message

    Examples:
        | Page           |
        | Methods        |
        | Tools          |
        | Use Cases      |
        | Organizations  |
        | Users          |


Scenario Outline: 6. admin checks pages's state after itsreviewer didn't submit publishing
    Given <Page> with user "admin" logged in
    Then "state" is "State: Private"
    And "state"'s name is "red"

    Examples:
        | Page           |
        | Methods        |
        | Tools          |
        | Use Cases      |
        | Organizations  |
        | Users          |