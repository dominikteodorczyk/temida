from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from scrapers.base import Scraper
import time
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
from utils.parsers import FortunaParser
from utils.events import (
    TwoWayBetEvent,
    ThreeWayBetEvent,
    TwoWayBetEventsTable,
    ThreeWayBetEventsTable,
)


class FortunaScraper(Scraper):
    def __init__(self, site_path: str) -> None:
        super().__init__(site_path)
        self.competition_boxes: list = []
        self.events_objects: list = []

    def close_cookie_msg(self):
        try:
            close_button = self.driver.find_element(
                By.XPATH, '//*[@id="cookie-consent-button-accept"]'
            )
            close_button.click()
        except Exception as e:
            print("Can't close cookies msg:", e)

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
        time.sleep(1)

    def get_segments(self):
        try:
            self.competition_boxes = self.driver.find_elements(
                By.XPATH, '//*[@id="sport-events-list-content"]/section[*]'
            )
        except NoSuchElementException as e:
            print(e)

    def get_all_events_objects(self):
        for box in self.competition_boxes:
            for event in box.find_elements(
                By.XPATH, ".//div[2]/div/div/table/tbody/tr[*]"
            ):
                if event.get_attribute("class") != "row-sub-markets":
                    self.events_objects.append(event)

    def get_events_from_site(self):
        try:
            self.close_cookie_msg()
            self.get_whole_site()
            self.get_whole_site()  # to be sure that whole site is unwraped
            self.get_segments()
            self.get_all_events_objects()
        except Exception as e:
            print(e)


class FortunaTwoWayBets(FortunaScraper):
    def __init__(self, site_path: str) -> None:
        super().__init__(site_path)
        self.events_data = TwoWayBetEventsTable("FORTUNA")

    def get_events_values(self):
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
            except NoSuchElementException as e:
                pass
            except Exception as e:
                print(e)


class FortunaThreeWayBets(FortunaScraper):
    def __init__(self, site_path: str) -> None:
        super().__init__(site_path)
        self.events_data = ThreeWayBetEventsTable("FORTUNA")

    def get_events_values(self):
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
            except NoSuchElementException as e:
                pass
            except Exception as e:
                print(e)
