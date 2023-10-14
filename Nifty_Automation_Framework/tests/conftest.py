import pytest
import allure
from allure_commons.types import AttachmentType
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


@pytest.fixture(scope="session")
def driver():
    driver_manager = webdriver.Chrome()
    yield driver_manager
    driver_manager.quit()