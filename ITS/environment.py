from selenium import webdriver
from selenium.webdriver import DesiredCapabilities


def before_all(context):
    context.browser = webdriver.Remote(
                command_executor='http://mys01.fit.vutbr.cz:4444/wd/hub',
                desired_capabilities=DesiredCapabilities.CHROME)
    context.browser.maximize_window()
    context.browser.implicitly_wait(15)

    context.address_url = "http://mys01.fit.vutbr.cz:8001"
    context.browser.get('http://mys01.fit.vutbr.cz:8001')

def after_all(context):
   context.browser.close()
