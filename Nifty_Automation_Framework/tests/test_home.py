import pytest
from pages.home_page import HomePage
from utils.logger import CustomLogger
from utils.utility import sort_the_dictionary

logger = CustomLogger(__name__, "log/equitymaster.log").get_logger()

@pytest.fixture(scope="class")
def home_page(driver):
    driver_manager = driver
    home_page = HomePage(driver_manager)
    home_page.navigate_to_home_page()
    yield home_page

class TestHome:
    @pytest.fixture(scope="class")
    def shared_top5_stocks(self):
        top5_stocks = {}
        yield top5_stocks


    def test_fetch_top5_stocks(self, shared_top5_stocks, home_page):
        company_profit_percentage = home_page.get_all_records()
        sorted_company_profit_percentage = sort_the_dictionary(company_profit_percentage)
        top_five_stocks = sorted_company_profit_percentage[:5]
        shared_top5_stocks.update(dict(top_five_stocks))
        logger.info(f"Top five stocks sorted manually {top_five_stocks}")

    def test_verify_top5_stocks(self, shared_top5_stocks, home_page):
        home_page.sort_by_clicking()
        top_five_stocks = home_page.fetch_top5_stocks()
        logger.info(f"Top five stocks sorted automatically {top_five_stocks}")
        assert top_five_stocks == shared_top5_stocks, "The top5 stocks are not matching"