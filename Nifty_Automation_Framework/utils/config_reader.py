import configparser

class ConfigReader:
    config = configparser.ConfigParser()
    config.read(r"C:\Users\Omprakash_Choudhari\PycharmProjects\Nifty_Automation_Framework\config.properties")

    @staticmethod
    def get_base_url():
        return ConfigReader.config.get('URLS', 'BASE_URL')