Feature: Compare two items

Scenario: Add products to Cart 
    Given page with "Laptops & Notebooks" 
    When click on button "Add to Cart" of item "Macbook Pro"
    And click on button "Add to Cart" of item "Sony VAIO"
    Then shopping cart shows "2" items in Cart

    Scenario: Compare two notebooks
    Given page "Laptops & Notebooks"
    When click on button "Compare this product" on Sony VIAO
    And appears message "Success: You have added Sony VAIO to your product comparison!"
    And click on button "Compare this product" on Macbook Pro
    And appears message "Success: You have added MacBook Pro to your product comparison!"
    And click on message "product comparison"
    Then appears page "Product Comparison"

    Scenario: Add product to cart from "Product Comparison" page
    Given page "Product Comparison"
    When click on button "Add to Cart" of items "Sony VIAO"
    Then appears message " Success: You have added Sony VAIO to your shopping cart!"

    Scenario: Go to shopping cart page from "Product Comparison" page
    Given page "Product Comparison"
    When click "shopping Cart" on "success" message 
    Then appears "Shopping Cart"

    Scenario: Delete product from Cart wich is 
    Given page "Shopping Cart"
    And "Shopping cart" shows items in Cart
    When click button "Remove" "1" item 
    Then page "Shopping Cart" shows Cart with "1" left item