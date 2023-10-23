"""
Module for the SuperbetScraper classes, a specialized scrapers for collecting
data from Superbet.

Classes:
---------
SuperbetScraper: A specialized scraper for collecting data from Superbet,
    inherits from Scraper.
SuperbetTwoWayBets(SuperbetScraper):A class representing a scraper for
    collecting two-way sports betting data from Superbet.
SuperbetThreeWayBets(SuperbetScraper): A class representing a scraper for
    collecting three-way sports betting data from Superbet.
"""
import traceback
import time
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from scrapers.base import Scraper
from utils.parsers import SuperbetParser
from utils.events import (
    TwoWayBetEvent,
    ThreeWayBetEvent,
    TwoWayBetEventsTable,
    ThreeWayBetEventsTable,
)
from utils.technical import setup_logger

class SuperbetScraper(Scraper):
    """
    A specialized scraper for collecting data from Superbet, inherits
    from Scraper.

    Attributes:
    -----------
    - site_path (str): The URL of the Superbet website.
    - events_objects (list): A dictionary to store event objects
        collected from Superbet.
    - logging (Logger): The logger for handling log messages.
    """

    def __init__(self, site_path: str) -> None:
        super().__init__(site_path)
        self.events_objects: list = []
        self.logging = setup_logger(name="SUPERBET", print_logs=True)
        self.logging.info(f"Starting to collect data: {self.site_path}")

    def close_cookie_msg(self):
        """
        Close the cookie message on the webpage.
        """
        try:
            close_button = self.driver.find_element(
                By.XPATH, '//*[@id="onetrust-accept-btn-handler"]'
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
        self.driver.execute_script("window.scrollTo(0, 0);")

    def get_events_from_site(self):
        """
        Attempts to collect events by closing cookie messages, scrolling
        through the entire site.
        """
        try:
            self.close_cookie_msg()
            self.get_whole_site()
            self.get_whole_site()
        except Exception as e:
            self.logging.error(f"Unknown bug, more here: {e}")
        self.logging.info(f"Events collected: {self.site_path}")


class SuperbetTwoWayBets(SuperbetScraper):
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
        self.events_data = TwoWayBetEventsTable("SUPERBET")

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
        height = self.driver.execute_script("return window.scrollY;")
        self.driver.execute_script("window.scrollTo(0, 0);")
        while True:
            elements = self.driver.find_elements(
                By.XPATH, '//*[contains(@id, "event-")]/div/div[1]'
            )
            for element in elements:
                try:
                    home_name = element.find_element(
                        By.XPATH, "./div[1]/div[2]/div[1]/span[1]"
                    ).text
                    away_name = element.find_element(
                        By.XPATH, "./div[1]/div[2]/div[1]/span[2]"
                    ).text
                    if f"{home_name}{away_name}" in self.events_objects:
                        pass
                    else:
                        event_data = {
                            "home_player": home_name,
                            "away_player": away_name,
                            "home_team_win": element.find_element(
                                By.XPATH,
                                "./div[2]/div[2]/div/div[1]/button/span[4]/span[2]",
                            ).text,
                            "away_team_win": element.find_element(
                                By.XPATH,
                                "./div[2]/div[2]/div/div[2]/button/span[4]/span[2]",
                            ).text,
                            "event_date": element.find_element(
                                By.XPATH,
                                "./div[1]/div[1]/span[1]",
                            ).text,
                        }
                        self.events_data.put(
                            TwoWayBetEvent.create_from_data(
                                event_data, SuperbetParser()
                            )
                        )
                        self.events_objects.append(f"{home_name}{away_name}")
                except NoSuchElementException:
                    pass
                except Exception as e:
                    exception_message = str(e)
                    traceback_str = traceback.format_exc()
                    self.logging.error(
                        f"Unknown bug, more here: {traceback_str} {exception_message}"
                    )
            self.driver.execute_script(
                f"window.scrollTo(0, window.scrollY + {4000});"
            )
            time.sleep(0.01)
            new_height = self.driver.execute_script("return window.scrollY;")
            if height == new_height:
                break
            height = new_height
        self.logging.info(f"Data collected: {self.site_path}")
        self.driver.quit()
        result_queue.put(self.events_data)


class SuperbetThreeWayBets(SuperbetScraper):
    """
    A class representing a scraper for collecting three-way sports betting
    data from Superbet.

    Inherits from:
    --------------
    SuperbetScraper

    Attributes:
    ------------
    events_data (ThreeWayBetEventsTable): An instance of the
    ThreeWayBetEventsTable class for storing and managing three-way
    sports betting event data.

    Parameters:
    -----------
    site_path (str): The URL of the Superbet webpage to scrape.
    """

    def __init__(self, site_path: str) -> None:
        super().__init__(site_path)
        self.events_data = ThreeWayBetEventsTable("SUPERBET")

    def get_events_values(self, result_queue):
        """
        Collects and processes three-way sports betting data from
        the Superbet webpage.

        This method scrapes and extracts relevant information
        from the Superbet webpage for three-way sports betting events.
        The collected data is then formatted and added to
        the ThreeWayBetEventsTable using the SuperbetParser.

        Parameters:
        -----------
        result_queue (Queue): A queue to store the result
        (ThreeWayBetEventsTable) for further processing.

        Returns:
        --------
        None
        """
        self.get_events_from_site()
        height = self.driver.execute_script("return window.scrollY;")
        self.driver.execute_script("window.scrollTo(0, 0);")
        while True:
            elements = self.driver.find_elements(
                By.XPATH, '//*[contains(@id, "event-")]/div/div[1]'
            )
            for element in elements:
                try:
                    home_name = element.find_element(
                        By.XPATH, "./div[1]/div[2]/div[1]/span[1]"
                    ).text
                    away_name = element.find_element(
                        By.XPATH, "./div[1]/div[2]/div[1]/span[2]"
                    ).text
                    if f"{home_name}{away_name}" in self.events_objects:
                        pass
                    else:
                        event_data = {
                            "home_player": home_name,
                            "away_player": away_name,
                            "home_team_win": element.find_element(
                                By.XPATH,
                                "./div[2]/div[2]/div/div[1]/button/span[4]/span[2]",
                            ).text,
                            "draw": element.find_element(
                                By.XPATH,
                                "./div[2]/div[2]/div/div[2]/button/span[4]/span[2]",
                            ).text,
                            "away_team_win": element.find_element(
                                By.XPATH,
                                "./div[2]/div[2]/div/div[3]/button/span[4]/span[2]",
                            ).text,
                            "event_date": element.find_element(
                                By.XPATH,
                                "./div[1]/div[1]/span[1]",
                            ).text,
                        }
                        self.events_data.put(
                            ThreeWayBetEvent.create_from_data(
                                event_data, SuperbetParser()
                            )
                        )
                        self.events_objects.append(f"{home_name}{away_name}")
                except NoSuchElementException:
                    pass
                except Exception as e:
                    exception_message = str(e)
                    traceback_str = traceback.format_exc()
                    self.logging.error(
                        f"Unknown bug, more here: {traceback_str} {exception_message}"
                    )
            self.driver.execute_script(
                f"window.scrollTo(0, window.scrollY + {4000});"
            )
            time.sleep(0.01)
            new_height = self.driver.execute_script("return window.scrollY;")
            if height == new_height:
                break
            height = new_height
        self.logging.info(f"Data collected: {self.site_path}")
        self.driver.quit()
        result_queue.put(self.events_data)
