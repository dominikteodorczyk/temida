"""
Module for the BetclicScraper classes, a specialized scrapers for collecting
data from Betclic.

Classes:
---------
BetclicScraper: A specialized scraper for collecting data from Betclic,
    inherits from Scraper.
BetclicTwoWayBets(BetclicScraper):A class representing a scraper for
    collecting two-way sports betting data from Betclic.
BetclicThreeWayBets(BetclicScraper): A class representing a scraper for
    collecting three-way sports betting data from Betclic.
"""

import time
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from scrapers.base import Scraper
from utils.parsers import BetclicParser
from utils.events import (
    TwoWayBetEvent,
    ThreeWayBetEvent,
    TwoWayBetEventsTable,
    ThreeWayBetEventsTable,
)
from utils.technical import setup_logger


class BetclicScraper(Scraper):
    """
    A specialized scraper for collecting data from Betclic, inherits
    from Scraper.

    Attributes:
    -----------
    - site_path (str): The URL of the Betclic website.
    - competition_boxes (list): A list to store competition boxes
        on the Betclic webpage.
    - events_objects (dict): A dictionary to store event objects
        collected from Betclic.
    - logging (Logger): The logger for handling log messages.
    """

    def __init__(self, site_path: str) -> None:
        super().__init__(site_path)
        self.competition_boxes: list = []
        self.events_objects: dict = {}
        self.logging = setup_logger(name="BETCLIC", print_logs=True)
        self.logging.info(f"Starting to collect data: {self.site_path}")

    def close_cookie_msg(self):
        """
        Close the cookie message on the webpage.
        """
        try:
            close_button = self.driver.find_element(
                By.XPATH, '//*[@id="popin_tc_privacy_button_2"]'
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
        last_height = self.driver.execute_script(
            "return document.body.scrollHeight"
        )
        while True:
            self.driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);"
            )
            time.sleep(3)
            new_height = self.driver.execute_script(
                "return document.body.scrollHeight"
            )
            if new_height == last_height:
                break
            last_height = new_height
        time.sleep(1)

    def get_segments(self):
        """
        Collect and store the segment elements from the current webpage.
        """
        try:
            boxes = self.driver.find_elements(
                By.XPATH,
                "/html/body/app-desktop/div[1]/div/bcdk-content-scroller/div/sports-all-offer/sports-events-list/bcdk-vertical-scroller/div/div[2]/div/div/div[*]",
            )
            for box in boxes:
                if (
                    box.get_attribute("class")
                    == "groupEvents ng-star-inserted"
                ) or (box.get_attribute("class") == "groupEvents"):
                    self.competition_boxes.append(box)
        except NoSuchElementException as e:
            self.logging.warning(f"No segment elements:{e}")

    def get_all_events_objects(self):
        """
        Collect and store all event objects from the current webpage.
        """
        for box in self.competition_boxes:
            for event in box.find_elements(
                By.XPATH, "./div[2]/sports-events-event[*]"
            ):
                self.events_objects[event] = box.find_element(
                    By.CLASS_NAME, "groupEvents_headTitle"
                ).text

    def get_events_from_site(self):
        """
        Attempts to collect events by closing cookie messages, scrolling
        through the entire site, extracting segments, and finally obtaining
        all event objects from the segments.
        """
        try:
            self.close_cookie_msg()
            self.get_whole_site()
            self.get_whole_site()
            self.get_segments()
            self.get_all_events_objects()
        except Exception as e:
            self.logging.error(f"Unknown bug, more here: {e}")
        self.logging.info(f"Events collected: {self.site_path}")


class BetclicTwoWayBets(BetclicScraper):
    """
    A class representing a scraper for collecting two-way sports betting
    data from Betclic.

    Inherits from:
    --------------
    BetclicScraper

    Attributes:
    ------------
    events_data (TwoWayBetEventsTable): An instance of the
    TwoWayBetEventsTable class for storing and managing two-way
    sports betting event data.

    Parameters:
    -----------
    site_path (str): The URL of the Betclic webpage to scrape.
    """

    def __init__(self, site_path: str) -> None:
        super().__init__(site_path)
        self.events_data = TwoWayBetEventsTable("BETCLIC")

    def get_events_values(self, result_queue) -> None:
        """
        Collects and processes two-way sports betting data from
        the Betclic webpage.

        This method scrapes and extracts relevant information
        from the Betclic webpage for two-way sports betting events.
        The collected data is then formatted and added to
        the TwoWayBetEventsTable using the BetclicParser.

        Parameters:
        -----------
        result_queue (Queue): A queue to store the result
        (TwoWayBetEventsTable) for further processing.

        Returns:
        --------
        None
        """
        self.get_events_from_site()
        for event, date in self.events_objects.items():
            try:
                event_data = {
                    "home_player": event.find_element(
                        By.XPATH,
                        "./a/div/scoreboards-scoreboard/scoreboards-scoreboard-global/div/div[1]/div",
                    ).text,
                    "away_player": event.find_element(
                        By.XPATH,
                        "./a/div/scoreboards-scoreboard/scoreboards-scoreboard-global/div/div[3]/div",
                    ).text,
                    "home_team_win": event.find_element(
                        By.XPATH,
                        "./a/sports-events-event-markets-v2/sports-markets-default-v2/div/sports-selections-selection[1]/div[1]/span[2]",
                    ).text,
                    "away_team_win": event.find_element(
                        By.XPATH,
                        "./a/sports-events-event-markets-v2/sports-markets-default-v2/div/sports-selections-selection[2]/div[1]/span[2]",
                    ).text,
                    "event_date": date,
                }
                self.events_data.put(
                    TwoWayBetEvent.create_from_data(
                        event_data, BetclicParser()
                    )
                )
            except NoSuchElementException:
                pass
            except Exception as e:
                self.logging.error(f"Unknown bug, more here: {e}")
        self.logging.info(f"Data collected: {self.site_path}")
        self.driver.quit()
        result_queue.put(self.events_data)


class BetclicThreeWayBets(BetclicScraper):
    """
    A class representing a scraper for collecting three-way sports betting
    data from Betclic.

    Inherits from:
    --------------
    BetclicScraper

    Attributes:
    ------------
    events_data (ThreeWayBetEventsTable): An instance of the
    ThreeWayBetEventsTable class for storing and managing three-way
    sports betting event data.

    Parameters:
    -----------
    site_path (str): The URL of the Betclic webpage to scrape.
    """

    def __init__(self, site_path: str) -> None:
        super().__init__(site_path)
        self.events_data = ThreeWayBetEventsTable("BETCLIC")

    def get_events_values(self, result_queue) -> None:
        """
        Collects and processes three-way sports betting data from
        the Betclic webpage.

        This method scrapes and extracts relevant information
        from the Betclic webpage for three-way sports betting events.
        The collected data is then formatted and added to
        the ThreeWayBetEventsTable using the BetclicParser.

        Parameters:
        -----------
        result_queue (Queue): A queue to store the result
        (ThreeWayBetEventsTable) for further processing.

        Returns:
        --------
        None
        """
        self.get_events_from_site()
        for event, date in self.events_objects.items():
            try:
                event_data = {
                    "home_player": event.find_element(
                        By.XPATH,
                        "./a/div/scoreboards-scoreboard/scoreboards-scoreboard-global/div/div[1]/div",
                    ).text,
                    "away_player": event.find_element(
                        By.XPATH,
                        "./a/div/scoreboards-scoreboard/scoreboards-scoreboard-global/div/div[3]/div",
                    ).text,
                    "home_team_win": event.find_element(
                        By.XPATH,
                        "./a/sports-events-event-markets-v2/sports-markets-default-v2/div/sports-selections-selection[1]/div/span[2]",
                    ).text,
                    "draw": event.find_element(
                        By.XPATH,
                        "./a/sports-events-event-markets-v2/sports-markets-default-v2/div/sports-selections-selection[2]/div/span[2]",
                    ).text,
                    "away_team_win": event.find_element(
                        By.XPATH,
                        "./a/sports-events-event-markets-v2/sports-markets-default-v2/div/sports-selections-selection[3]/div/span[2]",
                    ).text,
                    "event_date": date,
                }

                self.events_data.put(
                    ThreeWayBetEvent.create_from_data(
                        event_data, BetclicParser()
                    )
                )
            except NoSuchElementException:
                pass
            except Exception as e:
                self.logging.error(f"Unknown bug, more here: {e}")
        self.logging.info(f"Data collected: {self.site_path}")
        self.driver.quit()
        result_queue.put(self.events_data)
