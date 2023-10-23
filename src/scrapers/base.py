"""
Module for the Scraper class, a base class for web scraping using Selenium.

Classes:
---------
Scraper: A base class for web scraping using Selenium.
"""

from selenium import webdriver
from selenium.common.exceptions import SessionNotCreatedException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from utils.technical import setup_logger


class Scraper:
    """
    A base class for web scraping using Selenium.

    Attributes:
    -----------
    - site_path (object): The path or URL of the website to scrape.
    - driver (webdriver.Chrome): The Chrome WebDriver for interacting
        with the website.
    - logging (Logger): The logger for handling log messages.
    - wait (WebDriverWait): The WebDriverWait object for waiting for
        elements to load.
    """

    def __init__(self, site_path: object) -> None:
        self.site_path = site_path
        options = Options()
        options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(options=options)
        self.logging = setup_logger(name="BASE", print_logs=True)

        try:
            if self.site_path is not None:
                self.driver.get(site_path)
                self.wait = WebDriverWait(self.driver, 20)
            else:
                self.driver.quit()
                pass
        except SessionNotCreatedException as e:
            self.logging.info(f"URL error: {e}")
            self.driver.quit()

    @classmethod
    def init_with(cls, site_path):
        """
        Class method to create an instance of the Scraper class.

        Parameters:
        -----------
        - cls (class): The class (Scraper) that this method belongs to.
            site_path: The path or URL of the website to scrape.

        Returns:
        --------
        Scraper: An instance of the Scraper class.
        """
        return cls(site_path)
