from behave import *
import time
from selenium.webdriver.common.by import By

IMPLEMENTED_ERROR = NotImplementedError

use_step_matcher("re")


@given('page with "Laptops & Notebooks"')
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    time.sleep(1)
    context.browser.get("http://mys01.fit.vutbr.cz:8001/index.php?route=product/category&path=18")
    assert context.browser.current_url == "http://mys01.fit.vutbr.cz:8001/index.php?route=product/category&path=18"


@when('click on button "Add to Cart" of item "Macbook Pro"')
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    assert context.browser.find_element(By.CSS_SELECTOR,
                                 "#content > div:nth-child(9) > div:nth-child(4) > div > div:nth-child(2) > div.button-group > button:nth-child(1)")
    context.browser.find_element(By.CSS_SELECTOR,
                                 "#content > div:nth-child(9) > div:nth-child(4) > div > div:nth-child(2) > div.button-group > button:nth-child(1)").click()
    time.sleep(1)



@step('click on button "Add to Cart" of item "Sony VAIO"')
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    assert 'MacBook Pro' in context.browser.find_element(By.CSS_SELECTOR,
                                                         "body > div:nth-child(4) > div.alert.alert-success").text
    assert context.browser.find_element(By.CSS_SELECTOR,
                                 "#content > div:nth-child(9) > div:nth-child(5) > div > div:nth-child(2) > div.button-group > button:nth-child(1)")
    context.browser.find_element(By.CSS_SELECTOR,
                                 "#content > div:nth-child(9) > div:nth-child(5) > div > div:nth-child(2) > div.button-group > button:nth-child(1)").click()
    time.sleep(1)



@then('shopping cart shows "2" items in Cart')
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    assert 'Sony VAIO' in context.browser.find_element(By.CSS_SELECTOR,"body > div:nth-child(4) > div.alert.alert-success").text
    time.sleep(1)
    assert '2 item(s) - $3,202.00' in context.browser.find_element(By.CSS_SELECTOR, "#cart > button").text
    context.browser.find_element(By.CSS_SELECTOR, "#cart > button")



@given('page "Laptops & Notebooks"')
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    time.sleep(1)
    assert context.browser.current_url == "http://mys01.fit.vutbr.cz:8001/index.php?route=product/category&path=18"
    context.browser.get("http://mys01.fit.vutbr.cz:8001/index.php?route=product/category&path=18")


@when('click on button "Compare this product" on Sony VIAO')
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    assert context.browser.find_element(By.CSS_SELECTOR,
                                 "#content > div:nth-child(9) > div:nth-child(5) > div > div:nth-child(2) > div.button-group > button:nth-child(3)")
    context.browser.find_element(By.CSS_SELECTOR,
                                 "#content > div:nth-child(9) > div:nth-child(5) > div > div:nth-child(2) > div.button-group > button:nth-child(3)").click()
    time.sleep(1)





@step('click on button "Compare this product" on Macbook Pro')
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    assert context.browser.find_element(By.CSS_SELECTOR, "#content > div:nth-child(9) > div:nth-child(4) > div > div:nth-child(2) > div.button-group > button:nth-child(3)")
    context.browser.find_element(By.CSS_SELECTOR, "#content > div:nth-child(9) > div:nth-child(4) > div > div:nth-child(2) > div.button-group > button:nth-child(3)").click()
    time.sleep(1)


@step('click on message "product comparison"')
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    assert 'product comparison' in context.browser.find_element(By.CSS_SELECTOR,
                                                               "body > div:nth-child(4) > div.alert.alert-success").text
    context.browser.find_element_by_link_text('product comparison').click()
    time.sleep(1)


@then('appears page "Product Comparison"')
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    time.sleep(1)
    assert context.browser.current_url == "http://mys01.fit.vutbr.cz:8001/index.php?route=product/compare"
    context.browser.get("http://mys01.fit.vutbr.cz:8001/index.php?route=product/compare")



@given('page "Product Comparison"')
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    context.browser.get("http://mys01.fit.vutbr.cz:8001/index.php?route=product/compare")
    assert context.browser.current_url == "http://mys01.fit.vutbr.cz:8001/index.php?route=product/compare"


@when('click on button "Add to Cart" of items "Sony VIAO"')
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    assert context.browser.find_element(By.CSS_SELECTOR, "#content > table > tbody:nth-child(3) > tr > td:nth-child(2) > input")
    context.browser.find_element(By.CSS_SELECTOR, "#content > table > tbody:nth-child(3) > tr > td:nth-child(2) > input").click()
    time.sleep(1)


@step('click "shopping Cart" on "success" message')
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    assert 'shopping cart' in context.browser.find_element(By.CSS_SELECTOR, "body > div:nth-child(4) > div.alert.alert-success").text
    context.browser.find_element_by_link_text("shopping cart").click()
    time.sleep(1)


@then('appears "Shopping Cart"')
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    assert context.browser.current_url == "http://mys01.fit.vutbr.cz:8001/index.php?route=checkout/cart"
    context.browser.get("http://mys01.fit.vutbr.cz:8001/index.php?route=checkout/cart")



@given('page "Shopping Cart"')
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    assert context.browser.current_url == "http://mys01.fit.vutbr.cz:8001/index.php?route=checkout/cart"
    context.browser.get("http://mys01.fit.vutbr.cz:8001/index.php?route=checkout/cart")


@when('click button "Remove" "1" item "MacBook"')
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    assert context.browser.find_element(By.CSS_SELECTOR, "#content > form > div > table > tbody > tr:nth-child(1) > td:nth-child(4) > div > span > button.btn.btn-danger")
    context.browser.find_element(By.CSS_SELECTOR, "#content > form > div > table > tbody > tr:nth-child(1) > td:nth-child(4) > div > span > button.btn.btn-danger").click()
    time.sleep(2)



@then('page "Shopping Cart" shows Cart with "2" left item "Sony VAIO"')
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    assert 'Success: You have modified your shopping cart!' in context.browser.find_element(By.CSS_SELECTOR, "body > div:nth-child(4) > div.alert.alert-success").text
    context.browser.find_element(By.CSS_SELECTOR, "body > div:nth-child(4) > div.alert.alert-success")
    time.sleep(3)
