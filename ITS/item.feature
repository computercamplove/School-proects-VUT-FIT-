Feature: Creating new item and checking relations beetween items

    Scenario: 7. Try add new Item by Admin
    Given "Home" page with user "admin" logged in
    When click on "Add new"
    And click on <Item>
    Then appears Add <Item> Page

    Examples:
        | Item                |
        | Use Case            |
        | Evaluation Scenario |


    Scenario: 8. Error messages while creating new Use Case by Admin
    Given "Add Use Case" page
    When click on button "Save"
    Then appears "Error There were some errors." message
    And on <Input name> appears error "Required input is missing" message

    Examples:
        | Input name           |
        | Title                |
        | Use Case Description |


    Scenario: 9. Check relation between new Use Case and "Evaluation Scenario"
    Given "Add Use Case" page
    When add Title input "UC4 Test"
    And choose "UC4" in Use Case Number
    And choose "Aerospace" in Use Case Domain
    And search "fit" in Partners: Current Path
    And add input "test number 4" in Use Case Description
    And press button "Save"
    Then should appear Error message 
    But appears "Info Item created" message


    Scenario: 10. Check relation between "Evaluation Scenario" ad Requirements while submiting ES4 
    Given Add "Evaluation Scenario" page
    When add Title input "ES4 test"
    And add Id "UC4_R_1"
    And add "ES4 test" in "Evaluation Scenario Textual Description" 
    And press button "Save"
    Then should be Error message
    But Admin see "Info Item created"


    Scenario: 11. Move UC4 Test to Folder Use Cases by admin
    Given "Home" page with user "admin" logged in
    When click on Contents
    And click on button "Actions" on UC4 Test row
    And click on "Cut"
    And click on Folder Use Cases
    And click on button "Paste"
    Then appears "Successfully pasted items" message
    And UC4 Test appears in Folder Use Cases


    Scenario: 12. Make UC4 Test published by Admin
    Given: Use Cases Page
    When click on "UC4 Test"
    And click on "State: Private"
    And click on "Publish"
    Then appears "info Item state changed." message
    And color "state"'s name changes to "blue"


    Scenario: 13. Visitor (not logged in user) checks if new "UC4 Test" is published
    Given Visitor on page "Home"
    When click on "Use Cases" on navigation bar
    Then sees "UC4 Test" in the list of use cases




