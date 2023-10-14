from utils.logger import CustomLogger
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

logger = CustomLogger(__name__, "log/equitymaster.log").get_logger()

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.driver.maximize_window()

    def navigate(self, url):
        self.driver.get(url)

    def wait_for_element(self, locator, timeout=10):
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
        except TimeoutException:
            logger.error(f"Element not found within {timeout} seconds: {locator}")
            raise TimeoutException
    def get_element_text(self, locator):
        element = self.wait_for_element(locator)
        return element.text

    def click(self, locator):
        element = self.wait_for_element(locator)
        element.click()

    def scroll_to_locator(self, locator):
        element = self.wait_for_element(locator)
        self.driver.execute_script('arguments[0].scrollIntoView(true);', element)
