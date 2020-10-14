from behave import *
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
use_step_matcher("re")


@given('page with "Macbook Pro"')
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    time.sleep(1)
    context.browser.get("http://mys01.fit.vutbr.cz:8001/index.php?route=product/product&path=18&product_id=45")
    assert context.browser.current_url == "http://mys01.fit.vutbr.cz:8001/index.php?route=product/product&path=18&product_id=45"


@step("shopping cart shows 0 items")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    assert '0 item(s) - $0.00' in context.browser.find_element(By.CSS_SELECTOR, "#cart-total").text
    context.browser.find_element(By.CSS_SELECTOR, "#cart-total")
    time.sleep(1)



@when('fill "Qty" with 11 items - click add cart')
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    assert context.browser.find_element_by_name("quantity")
    element = context.browser.find_element_by_name("quantity")
    element.send_keys("1")
    time.sleep(1)
    assert context.browser.find_element(By.CSS_SELECTOR, "#button-cart")
    context.browser.find_element(By.CSS_SELECTOR, "#button-cart").click()
    time.sleep(1)

@then("shopping cart shows 11 items")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    assert '11 item(s) - $22,000.00' in context.browser.find_element(By.CSS_SELECTOR, "#cart > button").text
    context.browser.find_element(By.CSS_SELECTOR, "#cart > button")
    time.sleep(1)


@when('click button "Shopping cart"')
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    assert context.browser.find_element(By.CSS_SELECTOR, "#top-links > ul > li:nth-child(4) > a > i")
    context.browser.find_element(By.CSS_SELECTOR, "#top-links > ul > li:nth-child(4) > a > i")


@then('appears page "Shopping cart"')
def step_impl(context):
    """
    :type context: behave.runner.Context
    """

    context.browser.get("http://mys01.fit.vutbr.cz:8001/index.php?route=checkout/cart")
    assert context.browser.current_url == "http://mys01.fit.vutbr.cz:8001/index.php?route=checkout/cart"

    time.sleep(1)


@when('click on "Use Coupon Code"')
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    assert context.browser.find_element(By.CSS_SELECTOR, "#accordion > div:nth-child(1) > div.panel-heading > h4")
    context.browser.find_element(By.CSS_SELECTOR, "#accordion > div:nth-child(1) > div.panel-heading > h4 > a > i").click()
    time.sleep(1)


@step("appears area to enter code")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    assert context.browser.find_element(By.CSS_SELECTOR, "#collapse-coupon > div")
    context.browser.find_element(By.CSS_SELECTOR, "#collapse-coupon > div")
    time.sleep(3)

@step('fill "Enter your cupon here" with "ERTYU1233"')
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    assert context.browser.find_element_by_name("coupon")
    element = context.browser.find_element_by_name("coupon")
    element.send_keys("ERTYU1233")
    time.sleep(2)

@step('click button "Apply Coupon"')
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    assert context.browser.find_element(By.CSS_SELECTOR, "#button-coupon")
    context.browser.find_element(By.CSS_SELECTOR, "#button-coupon").click()
    time.sleep(1)



@then('appears "success" message')
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    assert context.browser.find_element(By.CSS_SELECTOR, "body > div:nth-child(4) > div.alert.alert-danger")
    context.browser.find_element(By.CSS_SELECTOR, "body > div:nth-child(4) > div.alert.alert-danger")
    time.sleep(1)
