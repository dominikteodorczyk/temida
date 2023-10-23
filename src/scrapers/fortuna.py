"""
Module for the FortunaScraper classes, a specialized scrapers for collecting
data from Fortuna.

Classes:
---------
FortunaScraper: A specialized scraper for collecting data from Fortuna,
    inherits from Scraper.
FortunaTwoWayBets(FortunaScraper):A class representing a scraper for
    collecting two-way sports betting data from Fortuna.
FortunaThreeWayBets(FortunaScraper): A class representing a scraper for
    collecting three-way sports betting data from Fortuna.
"""

import time
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from scrapers.base import Scraper
from utils.parsers import FortunaParser
from utils.events import (
    TwoWayBetEvent,
    ThreeWayBetEvent,
    TwoWayBetEventsTable,
    ThreeWayBetEventsTable,
)
from utils.technical import setup_logger


class FortunaScraper(Scraper):
    """
    A specialized scraper for collecting data from Fortuna, inherits
    from Scraper.

    Attributes:
    -----------
    - site_path (str): The URL of the Fortuna website.
    - competition_boxes (list): A list to store competition boxes
        on the Fortuna webpage.
    - events_objects (list): A dictionary to store event objects
        collected from Fortuna.
    - logging (Logger): The logger for handling log messages.
    """

    def __init__(self, site_path: str) -> None:
        super().__init__(site_path)
        self.competition_boxes: list = []
        self.events_objects: list = []
        self.logging = setup_logger(name="FORTUNA", print_logs=True)
        self.logging.info(f"Starting to collect data: {self.site_path}")

    def close_cookie_msg(self):
        """
        Close the cookie message on the webpage.
        """
        try:
            close_button = self.driver.find_element(
                By.XPATH, '//*[@id="cookie-consent-button-accept"]'
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
            self.competition_boxes = self.driver.find_elements(
                By.XPATH, '//*[@id="sport-events-list-content"]/section[*]'
            )
        except NoSuchElementException:
            self.logging.warning("No segment elements")

    def get_all_events_objects(self):
        """
        Collect and store all event objects from the current webpage.
        """
        for box in self.competition_boxes:
            for event in box.find_elements(
                By.XPATH, ".//div[2]/div/div/table/tbody/tr[*]"
            ):
                if event.get_attribute("class") != "row-sub-markets":
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
            self.get_whole_site()  # to be sure that whole site is unwraped
            self.get_segments()
            self.get_all_events_objects()
        except Exception as e:
            self.logging.error(f"Unknown bug, more here: {e}")
        self.logging.info(f"Events collected: {self.site_path}")


class FortunaTwoWayBets(FortunaScraper):
    """
    A class representing a scraper for collecting two-way sports betting
    data from Fortuna.

    Inherits from:
    --------------
    FortunaScraper

    Attributes:
    ------------
    events_data (TwoWayBetEventsTable): An instance of the
    TwoWayBetEventsTable class for storing and managing two-way
    sports betting event data.

    Parameters:
    -----------
    site_path (str): The URL of the Fortuna webpage to scrape.
    """

    def __init__(self, site_path: str) -> None:
        super().__init__(site_path)
        self.events_data = TwoWayBetEventsTable("FORTUNA")

    def get_events_values(self, result_queue):
        """
        Collects and processes two-way sports betting data from
        the Fortuna webpage.

        This method scrapes and extracts relevant information
        from the Fortuna webpage for two-way sports betting events.
        The collected data is then formatted and added to
        the TwoWayBetEventsTable using the FortunaParser.

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
                        By.XPATH, ".//td[1]/div/div[1]/span[1]"
                    ).text,
                    "away_player": event.find_element(
                        By.XPATH, ".//td[1]/div/div[1]/span[1]"
                    ).text,
                    "home_team_win": event.find_element(
                        By.XPATH, ".//td[2]/a/span"
                    ).text,
                    "away_team_win": event.find_element(
                        By.XPATH, ".//td[3]/a/span"
                    ).text,
                    "event_date": event.find_element(
                        By.CLASS_NAME, "event-datetime"
                    ).text,
                }
                if len(event_data["home_player"].split(" - ")) < 2:
                    pass
                else:
                    self.events_data.put(
                        TwoWayBetEvent.create_from_data(
                            event_data, FortunaParser()
                        )
                    )
            except NoSuchElementException:
                pass
            except Exception as e:
                self.logging.error(f"Unknown bug, more here: {e}")
        self.logging.info(f"Data collected: {self.site_path}")
        self.driver.quit()
        result_queue.put(self.events_data)


class FortunaThreeWayBets(FortunaScraper):
    """
    A class representing a scraper for collecting three-way sports betting
    data from Fortuna.

    Inherits from:
    --------------
    FortunaScraper

    Attributes:
    ------------
    events_data (ThreeWayBetEventsTable): An instance of the
    ThreeWayBetEventsTable class for storing and managing three-way
    sports betting event data.

    Parameters:
    -----------
    site_path (str): The URL of the Fortuna webpage to scrape.
    """

    def __init__(self, site_path: str) -> None:
        super().__init__(site_path)
        self.events_data = ThreeWayBetEventsTable("FORTUNA")

    def get_events_values(self, result_queue):
        """
        Collects and processes three-way sports betting data from
        the Fortuna webpage.

        This method scrapes and extracts relevant information
        from the Fortuna webpage for three-way sports betting events.
        The collected data is then formatted and added to
        the ThreeWayBetEventsTable using the FortunaParser.

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
                        By.XPATH, ".//td[1]/div/div[1]/span[1]"
                    ).text,
                    "away_player": event.find_element(
                        By.XPATH, ".//td[1]/div/div[1]/span[1]"
                    ).text,
                    "home_team_win": event.find_element(
                        By.XPATH, ".//td[2]/a/span"
                    ).text,
                    "draw": event.find_element(
                        By.XPATH, ".//td[3]/a/span"
                    ).text,
                    "away_team_win": event.find_element(
                        By.XPATH, ".//td[4]/a/span"
                    ).text,
                    "event_date": event.find_element(
                        By.CLASS_NAME, "event-datetime"
                    ).text,
                }
                if len(event_data["home_player"].split(" - ")) < 2:
                    pass
                else:
                    self.events_data.put(
                        ThreeWayBetEvent.create_from_data(
                            event_data, FortunaParser()
                        )
                    )
            except NoSuchElementException:
                pass
            except Exception as e:
                self.logging.error(f"Unknown bug, more here: {e}")
        self.logging.info(f"Data collected: {self.site_path}")
        self.driver.quit()
        result_queue.put(self.events_data)
