import traceback
import time
from scrapers.base import Scraper
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from utils.parsers import ForbetParser
from utils.events import (
    TwoWayBetEvent,
    ThreeWayBetEvent,
    TwoWayBetEventsTable,
    ThreeWayBetEventsTable,
)


class ForbetScraper(Scraper):
    def __init__(self, site_path: str) -> None:
        super().__init__(site_path)
        self.main_boxes: list = []
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
            time.sleep(5)
            confirm_button = self.driver.find_element(
                By.XPATH, "/html/body/div[1]/div[1]/div/div/div[2]/button[3]"
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
                By.XPATH,
                '//*[@id="__next"]/div/div/main/div/div/div/div/div[1]/section/div/section[*]',
            )
            for box in _main_boxes:
                self.main_boxes.append(box)
        except NoSuchElementException:
            self.logging.warning("No segment elements")

    def get_competition_boxes(self):
        for box in self.main_boxes:
            competition_box = box.find_elements(By.XPATH, ".//div/section[*]")
            for comp_box in competition_box:
                self.competition_boxes.append(comp_box)

    def get_events_from_site(self):
        try:
            self.close_adult_msg()
            self.close_cookies_msg()
            self.get_main_sections()
            self.get_competition_boxes()
        except Exception as e:
            self.logging.error(f"Unknown bug, more here: {e}")

        self.logging.info(f"Events collected: {self.site_path}")


class ForbetTwoWayBets(ForbetScraper):
    """
    A class representing a scraper for collecting two-way sports betting
    data from Superbet.

    Inherits from:
    --------------
    SuperbetScraper

    Attributes:
    ------------
    events_data (TwoWayBetEventsTable): An instance of the
    TwoWayBetEventsTable class for storing and managing two-way
    sports betting event data.

    Parameters:
    -----------
    site_path (str): The URL of the Superbet webpage to scrape.
    """

    def __init__(self, site_path: str) -> None:
        super().__init__(site_path)
        self.events_data = TwoWayBetEventsTable("FORBET")

    def get_events_values(self, result_queue):
        """
        Collects and processes two-way sports betting data from
        the Superbet webpage.

        This method scrapes and extracts relevant information
        from the Superbet webpage for two-way sports betting events.
        The collected data is then formatted and added to
        the TwoWayBetEventsTable using the SuperbetParser.

        Parameters:
        -----------
        result_queue (Queue): A queue to store the result
        (TwoWayBetEventsTable) for further processing.

        Returns:
        --------
        None
        """
        self.get_events_from_site()
        for element in self.competition_boxes:
            raw_date = element.find_element(By.XPATH,'.//header/h3').text
            for event in element.find_elements(
                By.XPATH,
                './/div[*]'
            ):
                try:
                    event_data = {
                        "home_player": event.find_element(
                            By.XPATH, ".//a[1]/header"
                        ).text,
                        "away_player": event.find_element(
                            By.XPATH, ".//a[1]/header"
                        ).text,
                        "home_team_win": event.find_element(
                            By.XPATH,
                            ".//div[3]/div[1]/button[1]",
                        ).text,
                        "away_team_win": event.find_element(
                            By.XPATH,
                            ".//div[3]/div[1]/button[2]",
                        ).text,
                        "event_date": raw_date,
                    }
                    self.events_data.put(
                        TwoWayBetEvent.create_from_data(
                            event_data, ForbetParser()
                        )
                    )
                except NoSuchElementException as e:
                    pass
                except Exception as e:
                    exception_message = str(e)
                    traceback_str = traceback.format_exc()
                    self.logging.error(
                        f"Unknown bug, more here: {traceback_str} {exception_message}"
                    )
        self.logging.info(f"Data collected: {self.site_path}")
        # self.driver.quit()
        result_queue.put(self.events_data)
