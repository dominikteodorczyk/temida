"""
Module for the STSScraper classes, a specialized scrapers for collecting
data from STS.

Classes:
---------
STSScraper: A specialized scraper for collecting data from STS,
    inherits from Scraper.
STSTwoWayBets(STSScraper):A class representing a scraper for
    collecting two-way sports betting data from STS.
STSThreeWayBets(STSScraper): A class representing a scraper for
    collecting three-way sports betting data from STS.
"""

import time
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from scrapers.base import Scraper
from utils.parsers import STSParser
from utils.events import (
    TwoWayBetEvent,
    ThreeWayBetEvent,
    TwoWayBetEventsTable,
    ThreeWayBetEventsTable,
)
from utils.technical import setup_logger


class STSScraper(Scraper):
    """
    A specialized scraper for collecting data from STS, inherits
    from Scraper.

    Attributes:
    -----------
    - site_path (str): The URL of the STS website.
    - competition_boxes (list): A list to store competition boxes
        on the STS webpage.
    - events_objects (list): A dictionary to store event objects
        collected from STS.
    - logging (Logger): The logger for handling log messages.
    """

    def __init__(self, site_path: str) -> None:
        super().__init__(site_path)
        self.competition_boxes: list = []
        self.events_objects: list = []
        self.logging = setup_logger(name="STS", print_logs=True)
        self.logging.info(f"Starting to collect data: {self.site_path}")

    def close_cookie_msg(self):
        """
        Close the cookie message on the webpage.
        """
        try:
            close_button = self.driver.find_element(
                By.XPATH,
                '//*[@id="CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll"]',
            )
            close_button.click()
        except NoSuchElementException:
            self.logging.warning("Can't close cookies msg")
        except Exception as e:
            self.logging.error(f"Unknown bug, more here: {e}")

    def get_whole_site(self):
        """
        Scroll through the entire webpage to ensure all content is loaded.
        """
        while True:
            try:
                close_button = self.driver.find_element(
                    By.XPATH,
                    "/html/body/app-mweb/div/div/div/div[1]/div/div[2]/app-prematch/app-sport/div[2]/app-popular/div/app-show-more-container/app-show-more-progress-info/div/sts-shared-static-button/button/span/span[2]/span",
                )
                close_button.click()
                time.sleep(0.5)
            except NoSuchElementException:
                break
            except Exception as e:
                self.logging.error(f"Unknown bug, more here: {e}")

    def get_segments(self):
        """
        Collect and store the segment elements from the current webpage.
        """
        try:
            self.competition_boxes = self.driver.find_elements(
                By.XPATH,
                "/html/body/app-mweb/div/div/div/div[1]/div/div[2]/app-prematch/app-sport/div[2]/app-popular/div/app-show-more-container/bb-leagues-wrapper/bb-league[*]",
            )
        except NoSuchElementException:
            self.logging.warning("No segment elements")

    def get_all_events_objects(self):
        """
        Collect and store all event objects from the current webpage.
        """
        for box in self.competition_boxes:
            for event in box.find_elements(
                By.XPATH, "./div/div[2]/bb-match[*]"
            ):
                self.events_objects.append(event)

    def get_events_from_site(self):
        """
        Attempts to collect events by closing cookie messages, scrolling
        through the entire site, extracting segments, and finally obtaining
        all event objects from the segments.
        """
        try:
            self.close_cookie_msg()
            self.get_whole_site()
            self.get_segments()
            self.get_all_events_objects()
        except Exception as e:
            self.logging.error(f"Unknown bug, more here: {e}")
        self.logging.info(f"Events collected: {self.site_path}")


class STSTwoWayBets(STSScraper):
    """
    A class representing a scraper for collecting two-way sports betting
    data from STS.

    Inherits from:
    --------------
    STSScraper

    Attributes:
    ------------
    events_data (TwoWayBetEventsTable): An instance of the
    TwoWayBetEventsTable class for storing and managing two-way
    sports betting event data.

    Parameters:
    -----------
    site_path (str): The URL of the STS webpage to scrape.
    """

    def __init__(self, site_path: str) -> None:
        super().__init__(site_path)
        self.events_data = TwoWayBetEventsTable("STS")

    def get_events_values(self, result_queue):
        """
        Collects and processes two-way sports betting data from
        the STS webpage.

        This method scrapes and extracts relevant information
        from the STS webpage for two-way sports betting events.
        The collected data is then formatted and added to
        the TwoWayBetEventsTable using the STSParser.

        Parameters:
        -----------
        result_queue (Queue): A queue to store the result
        (TwoWayBetEventsTable) for further processing.

        Returns:
        --------
        None
        """
        self.get_events_from_site()
        for event in self.events_objects:
            try:
                event_data = {
                    "home_player": event.find_element(
                        By.XPATH,
                        "./div/div[2]/div[1]/a/bb-score/div/div/div/p[1]",
                    ).text,
                    "away_player": event.find_element(
                        By.XPATH,
                        "./div/div[2]/div[1]/a/bb-score/div/div/div/p[2]",
                    ).text,
                    "home_team_win": event.find_element(
                        By.XPATH,
                        "./div/div[2]/div[2]/bb-opportunity/div/div/bb-odd[1]/div/div/div[2]",
                    ).text,
                    "away_team_win": event.find_element(
                        By.XPATH,
                        "./div/div[2]/div[2]/bb-opportunity/div/div/bb-odd[2]/div/div/div[2]",
                    ).text,
                    "event_date": event.find_element(
                        By.XPATH,
                        "./div/div[1]/div[1]/a/bb-score-header/div/div/div/div/span[1]",
                    ).text,
                }
                self.events_data.put(
                    TwoWayBetEvent.create_from_data(event_data, STSParser())
                )
            except NoSuchElementException:
                pass
            except Exception as e:
                self.logging.error(f"Unknown bug, more here: {e}")
        self.logging.info(f"Data collected: {self.site_path}")
        self.driver.quit()
        result_queue.put(self.events_data)


class STSThreeWayBets(STSScraper):
    """
    A class representing a scraper for collecting three-way sports betting
    data from STS.

    Inherits from:
    --------------
    STSScraper

    Attributes:
    ------------
    events_data (ThreeWayBetEventsTable): An instance of the
    ThreeWayBetEventsTable class for storing and managing three-way
    sports betting event data.

    Parameters:
    -----------
    site_path (str): The URL of the STS webpage to scrape.
    """

    def __init__(self, site_path: str) -> None:
        super().__init__(site_path)
        self.events_data = ThreeWayBetEventsTable("STS")

    def get_events_values(self, result_queue):
        """
        Collects and processes three-way sports betting data from
        the STS webpage.

        This method scrapes and extracts relevant information
        from the STS webpage for three-way sports betting events.
        The collected data is then formatted and added to
        the ThreeWayBetEventsTable using the STSParser.

        Parameters:
        -----------
        result_queue (Queue): A queue to store the result
        (ThreeWayBetEventsTable) for further processing.

        Returns:
        --------
        None
        """
        self.get_events_from_site()
        for event in self.events_objects:
            try:
                event_data = {
                    "home_player": event.find_element(
                        By.XPATH,
                        "./div/div[2]/div[1]/a/bb-score/div/div/div/p[1]",
                    ).text,
                    "away_player": event.find_element(
                        By.XPATH,
                        "./div/div[2]/div[1]/a/bb-score/div/div/div/p[2]",
                    ).text,
                    "home_team_win": event.find_element(
                        By.XPATH,
                        "./div/div[2]/div[2]/bb-opportunity/div/div/bb-odd[1]/div/div/div[2]",
                    ).text,
                    "draw": event.find_element(
                        By.XPATH,
                        "./div/div[2]/div[2]/bb-opportunity/div/div/bb-odd[2]/div/div/div[2]",
                    ).text,
                    "away_team_win": event.find_element(
                        By.XPATH,
                        "./div/div[2]/div[2]/bb-opportunity/div/div/bb-odd[3]/div/div/div[2]",
                    ).text,
                    "event_date": event.find_element(
                        By.XPATH,
                        "./div/div[1]/div[1]/a/bb-score-header/div/div/div/div/span[1]",
                    ).text,
                }
                self.events_data.put(
                    ThreeWayBetEvent.create_from_data(event_data, STSParser())
                )
            except NoSuchElementException:
                pass
            except Exception as e:
                self.logging.error(f"Unknown bug, more here: {e}")
        self.logging.info(f"Data collected: {self.site_path}")
        self.driver.quit()
        result_queue.put(self.events_data)
