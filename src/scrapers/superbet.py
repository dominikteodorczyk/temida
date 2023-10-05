from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from scrapers.base import Scraper
import time
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.parsers import SuperbetParser
from utils.events import (
    TwoWayBetEvent,
    ThreeWayBetEvent,
    TwoWayBetEventsTable,
    ThreeWayBetEventsTable,
)
from utils.technical import setup_logger
import traceback


class SuperbetScraper(Scraper):
    def __init__(self, site_path: str) -> None:
        super().__init__(site_path)
        self.events_objects: list = []
        self.logging = setup_logger(name="SUPERBET", print_logs=True)
        self.logging.info(f"Starting to collect data: {self.site_path}")

    def close_cookie_msg(self):
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

    def get_segments(self):
        pass

    def get_events_from_site(self):
        try:
            self.close_cookie_msg()
            self.get_whole_site()
            self.get_whole_site()
            self.get_segments()
        except Exception as e:
            self.logging.error(f"Unknown bug, more here: {e}")
        self.logging.info(f"Events collected: {self.site_path}")


class SuperbetTwoWayBets(SuperbetScraper):
    def __init__(self, site_path: str) -> None:
        super().__init__(site_path)
        self.events_data = TwoWayBetEventsTable("SUPERBET")

    def get_events_values(self, result_queue):
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
                except NoSuchElementException as e:
                    pass
                except Exception as e:
                    exception_message = str(e)
                    traceback_str = traceback.format_exc()
                    self.logging.error(f"Unknown bug, more here: {traceback_str} {exception_message}")
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
        result_queue.put(self.events_data.data)

class SuperbetThreeWayBets(SuperbetScraper):
    def __init__(self, site_path: str) -> None:
        super().__init__(site_path)
        self.events_data = ThreeWayBetEventsTable("SUPERBET")

    def get_events_values(self, result_queue):
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
                except NoSuchElementException as e:
                    pass
                except Exception as e:
                    exception_message = str(e)
                    traceback_str = traceback.format_exc()
                    self.logging.error(f"Unknown bug, more here: {traceback_str} {exception_message}")
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
        result_queue.put(self.events_data.data)