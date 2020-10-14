Feature: Online shoping notebook in opencart

    Scenario Outline: Add products to Cart 
    Given page with "Macbook Pro"
    And shopping cart shows <start> items
    When fill "Qty" with <add> items  
    And click on button "Add to Cart"
    Then shopping cart shows <total> items

    Examples:
    | start |  add  | total |
    |   0   |   1   |   1   |
    |   1   |   1   |   2   |

    Scenario: Go to page "Shopping cart"
    Given page with "Macbook Pro"
    When click button "Shopping cart"
    Then appears page "Shopping cart"

    Scenario: update amount of items
    Given page "Shopping Cart"
    When click on "Quantity" area
    And change amount of items from "2" to "3"
    And click button "Update"
    Then "Quantity" changed on "3" items
    And "Total price" changed in 3 times

    Scenario: Use coupon code
    Given page "Shopping Cart"
    When click on "Use Coupon Code"
    And appears area to enter code
    And fill "Enter your cupon here" with "ERTYU1233"
    And click button "Apply Coupon"
    Then appears "success" message
    
    Scenario: Estimate Shipping & Taxes
    Given page "Shopping Cart"
    When click on "Estimate Shipping & Taxes"
    And appears area with "Enter your destination to get a shipping estimate"
    And choose country "Czech Republic" in "Country"
    And choose region "Jihomoravsky" in "Region / State" 
    And fill "Post Code" - "61200"
    And click button "Get Quotes"
    And appears pop-up window "to choose shipping method"
    And click on "Flat Shipping Rate"
    And click on button "Apply"
    Then appears message "Success: Your shipping estimate has been applied!"

    Scenario: page checkout
    Given page "Shopping Cart"
    When click on button "Checkout"
    Then appears page "Checkout"

    Scenario: 1 step of checkout
    Given page "Checkout"
    And "Step 1" options
    When choose "Guest Checkout"
    And click "Continue"
    Then appears "Step 2: Billing Details" options

    Scenario: 2 step of checkout
    Given page "Checkout"
    And "Step 2" options
    When fill "First Name" with "Guest"
    And fill "Last Name" with "Guest"
    And fill "E-Mail" with "xabike00"
    And fill "Telephone" with "1234567890"
    And fill "Address 1" with "Kolejni 2"
    And fill "City" with "Brno"
    And fill "Post Code" with "61200"
    And choose country "Czech Republic" in "Country"
    And choose region "Jihomoravsky" in "Region / State"
    And click on ckeckbox "My delivery and billing addresses are the same"
    And click "Continue"
    Then appears "Step 4: Delivery Method" options

    Scenario: 4 step of checkout
    Given page "Checkout"
    And "Step 4" options
    When click "Continue"
    Then appears "Step 5: Payment Method" options

    Scenario: 5 step of checkout
    Given page "Checkout"
    And "Step 5" options
    When click on ckeckbox "I have read and agree to the Terms & Conditions"
    And click "Continue"
    Then appears "Step 6: Confirm Order" options

    Scenario: 6 step of checkout
    Given page "Checkout"
    And "Step 6" options
    When click "Confirm Order"
    Then appears page "Success" with message "Your order has been placed!"

    Scenario: Contact form
    Given page "Success"
    When click on link "store owner"
    And show up page "Contact Us" with "Contact Form"
    And fill "Your name" with "xabike"
    And fill "E-Mail Address" with "xabike@mail.com"
    And fill "Enqury" with "Want to change address of shipping"
    And click button "Submit"
    Then appears page "Contact Us" with button "Continue"
    And click on button "Continue"
    And appears main page "opencart"