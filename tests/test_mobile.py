import allure
import pytest
import os
from allure_commons._allure import step
from appium.webdriver.common.appiumby import AppiumBy
from selene import have
from dotenv import load_dotenv
from appium import webdriver
from datetime import date
from selene.support.shared import browser
from utilities.attachment import add_video


@pytest.fixture(scope='session', autouse=True)
def load_env():
    load_dotenv()


@pytest.fixture(scope='function')
def init():
    USER = os.getenv('LOGIN', 'daniilmatafonov1')
    KEY = os.getenv('KEY', 'BdGpepMx8e9EhhxExqqj')
    APPIUM_BROWSERSTACK = os.getenv('APPIUM_BROWSERSTACK', 'hub-cloud.browserstack.com')
    desired_cap = {
        "app": "bs://c700ce60cf13ae8ed97705a55b8e022f13c5827c",
        "deviceName": "Google Pixel 3",
        "platformVersion": "9.0",
        "platformName": "android",
        "project": "Python project",
        "build": "browserstack-build-" + str(date.today()),
        'bstack:options': {
            "projectName": "Mobile tests",
            "buildName": "browserstack-build-DEMO2",
            "sessionName": "BStack second_test"
        }
    }
    browser.config.driver = webdriver.Remote(
        command_executor=f"https://{USER}:{KEY}@{APPIUM_BROWSERSTACK}/wd/hub",
        desired_capabilities=desired_cap
    )
    browser.config.timeout = 4
    yield init
    browser.quit()


@allure.tag('mobile')
@allure.title('Test search')
def test_wiki_browserstack(init):
    with step('Type search'):
        browser.element((AppiumBy.ACCESSIBILITY_ID, 'Search Wikipedia')).click()
        browser.element((AppiumBy.ID, "org.wikipedia.alpha:id/search_src_text")).type('BrowserStack')
    with step('Verify content found'):
        browser.all((AppiumBy.ID, 'org.wikipedia.alpha:id/page_list_item_title'))\
            .should(have.size_greater_than(0))
    add_video(browser)


@allure.tag('mobile')
@allure.title('Test search')
def test_wiki_sqa(init):
    with step('Type search'):
        browser.element((AppiumBy.ACCESSIBILITY_ID, 'Search Wikipedia')).click()
        browser.element((AppiumBy.ID, "org.wikipedia.alpha:id/search_src_text")).type("Software quality assurance")
    with step('Verify content found'):
        browser.all(
            (AppiumBy.ID, 'org.wikipedia.alpha:id/page_list_item_title')
        ).should(have.size_greater_than(0))
    add_video(browser)