## Project 1 - Test plan for Opencart website ##

Author: Zhamilya Abikenova 

Tests were written in BDD approach for Opencart website 

### References ###

- [Opencart](http://mys01.fit.vutbr.cz:8001/index.php?route=common/home) website

### Features to be tested ###
- Basic buying process from adding item to cart to finish order
- Compare two products which user had already in cart

### `buying.feature` ###
##### Required details #####
- Item
- Coupon code
- First Name
- Last Name
- E-Mail
- Address
- City
- Telephone
- Text for additional information

Adding items to cart. Updating number of items in cart. Using coupon for order. Estimating Shipping & Taxes. Going to page "Checkout". Choosing "Guest Checkout". Filling name and address. Agreeing with Terms & Conditions in "Payment Method". Confirming order. After confirming order writting to owner ("Contact Us") to change information in order.

### `compare_items.feature` ###
##### Required details #####
- Items for comparing

Add two items to cart. Product comparison of the two items. Adding "Sony VIAO" and "Macbook Pro" to "Product Comparison". Adding item "Sony VIAO" to cart. Going to page "Shipping Cart". Deleting item "Macbook Pro" from cart.
