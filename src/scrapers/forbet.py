import time
from scrapers.base import Scraper
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


class ForbetScraper(Scraper):
    def __init__(self, site_path: str) -> None:
        super().__init__(site_path)
        self.competition_boxes: list = []
        self.events_objects: dict = {}


    def close_adult_msg(self):
        try:
            confirm_button = self.driver.find_element(
                By.XPATH, '//*[@id="adultConfirmation"]/div/button[1]'
            )
            confirm_button.click()
        except NoSuchElementException:
            self.logging.warning("Can't close adult msg")
        except Exception as e:
            self.logging.error(f"Unknown bug, more here: {e}")

    def close_cookies_msg(self):
        try:
            confirm_button = self.driver.find_element(
                By.XPATH, '/html/body/div[1]/div[1]/div/div/div[2]/button[3]'
            )
            confirm_button.click()
        except NoSuchElementException:
            self.logging.warning("Can't close adult msg")
        except Exception as e:
            self.logging.error(f"Unknown bug, more here: {e}")

    def get_events_from_site(self):

        try:
            self.close_adult_msg()
            self.close_cookies_msg
        except Exception as e:
            self.logging.error(f"Unknown bug, more here: {e}")
        self.logging.info(f"Events collected: {self.site_path}")
