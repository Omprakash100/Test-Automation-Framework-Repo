from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from pages.base_page import BasePage
from utils.config_reader import ConfigReader
from utils.logger import CustomLogger
from pages.custom_exceptions import ClosePopup, PercentageNotPresent

logger = CustomLogger(__name__, "log/equitymaster.log").get_logger()

class HomePage(BasePage):
    RECORDS = (By.XPATH, "//table[@class='mystocks cls']/tbody/tr")
    POPUP = (By.XPATH, "//button[@title='Close' and @tabindex]")
    BSE_PRICE_BUTTON = (By.PARTIAL_LINK_TEXT, "BSE PRICE")

    def __init__(self, driver):
        super().__init__(driver)
        self.url = ConfigReader.get_base_url()
        logger.info("Equitymaster Homepage initialized")

    def navigate_to_home_page(self):
        logger.info("Navigating to Equitymaster: %s", self.url)
        self.navigate(self.url)

    def load_next_elements(self, locator, index):
        try:
            dynamic_xpath = locator[1] + f"[{index}]"
            locator = (locator[0], dynamic_xpath.format(index))
            self.scroll_to_locator(locator)
        except TimeoutException:
            raise StopIteration

    def get_name_and_profit(self, index):
        try:
            company_name = self.get_element_text((By.XPATH, f"//table[@class='mystocks cls']/tbody/tr[{index}]/td[1]"))
            is_percentage_exists = self.get_element_text((By.XPATH, f"//table[@class='mystocks cls']/tbody/tr[{index}]/td[2]"))
            if is_percentage_exists == 'Not Listed':
                logger.warning(f"Profit percentage does not exist for {company_name}")
                raise PercentageNotPresent
            profit_percentage = self.get_element_text((By.XPATH, f"//table[@class='mystocks cls']/tbody/tr[{index}]/td[2]/small"))
            if company_name == '' or profit_percentage == '':
                raise ClosePopup
            else:
                return (company_name, profit_percentage)
        except (TimeoutException, ClosePopup):
            try:
                self.click(self.POPUP)
                logger.warning("Popup detected, Closing the Popup")
                raise ClosePopup
            except TimeoutException:
                raise StopIteration


    def fetch_all_records(self):
        company_profit_percentage = {}
        i = 1
        while True:
            try:
                if (i % 100 == 85):
                    logger.info(f"Loading elements from index {i}")
                    self.load_next_elements(self.RECORDS, index=i)
                company_name, profit_percentage = self.get_name_and_profit(index=i)
                company_profit_percentage[company_name] = float(profit_percentage.strip('%'))
                i += 1
            except PercentageNotPresent:
                i += 1
            except ClosePopup:
                continue
            except StopIteration:
                break
        return company_profit_percentage

    def get_all_records(self):
        logger.info("Fetching stocks Value")
        return self.fetch_all_records()

    def sort_by_clicking(self):
        self.click(self.BSE_PRICE_BUTTON)

    def fetch_top5_stocks(self):
        company_profit_percentage = {}
        for i in range(1,6):
            company_name, profit_percentage = self.get_name_and_profit(index=i)
            company_profit_percentage[company_name] = float(profit_percentage.strip('%'))
        return company_profit_percentage


