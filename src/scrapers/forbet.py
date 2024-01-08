import time
from scrapers.base import Scraper
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


class ForbetScraper(Scraper):
    def __init__(self, site_path: str) -> None:
        super().__init__(site_path)
        self.main_boxes: list = []
        self.competition_boxes: dict = {}
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
            time.sleep(5)
            confirm_button = self.driver.find_element(
                By.XPATH, '/html/body/div[1]/div[1]/div/div/div[2]/button[3]'
            )
            confirm_button.click()
        except NoSuchElementException:
            self.logging.warning("Can't close adult msg")
        except Exception as e:
            self.logging.error(f"Unknown bug, more here: {e}")

    def get_main_sections(self):
        """
        Collect and store the main events segment elements from the
        current webpage.
        """
        time.sleep(5)
        try:
            _main_boxes = self.driver.find_elements(
                By.XPATH, '//*[@id="__next"]/div/div/main/div/div/div/div/div[1]/section/div/section[*]'
            )
            for box in _main_boxes:
                self.main_boxes.append(box)
        except NoSuchElementException:
            self.logging.warning("No segment elements")


    def get_events_from_site(self):

        try:
            self.close_adult_msg()
            self.close_cookies_msg()
            self.get_main_sections()
        except Exception as e:
            self.logging.error(f"Unknown bug, more here: {e}")


        self.logging.info(f"Events collected: {self.site_path}")
