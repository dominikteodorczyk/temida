from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from scrapers.base import Scraper
import time
from utils.parsers import STSParser
from utils.events import (
    TwoWayBetEvent,
    ThreeWayBetEvent,
    TwoWayBetEventsTable,
    ThreeWayBetEventsTable,
)
from utils.technical import setup_logger


class STSScraper(Scraper):
    def __init__(self, site_path: str) -> None:
        super().__init__(site_path)
        self.competition_boxes: list = []
        self.events_objects: list = []
        self.logging = setup_logger(name="STS", print_logs=True)
        self.logging.info(f"Starting to collect data: {self.site_path}")

    def close_cookie_msg(self):
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
        try:
            self.competition_boxes = self.driver.find_elements(
                By.XPATH,
                "/html/body/app-mweb/div/div/div/div[1]/div/div[2]/app-prematch/app-sport/div[2]/app-popular/div/app-show-more-container/bb-leagues-wrapper/bb-league[*]",
            )
        except NoSuchElementException as e:
            self.logging.warning(f"No segment elements")

    def get_all_events_objects(self):
        for box in self.competition_boxes:
            for event in box.find_elements(
                By.XPATH, "./div/div[2]/bb-match[*]"
            ):
                self.events_objects.append(event)

    def get_events_from_site(self):
        try:
            self.close_cookie_msg()
            self.get_whole_site()
            self.get_segments()
            self.get_all_events_objects()
        except Exception as e:
            self.logging.error(f"Unknown bug, more here: {e}")
        self.logging.info(f"Events collected: {self.site_path}")



class STSTwoWayBets(STSScraper):
    def __init__(self, site_path: str) -> None:
        super().__init__(site_path)
        self.events_data = TwoWayBetEventsTable("STS")

    def get_events_values(self, result_queue):
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
            except NoSuchElementException as e:
                pass
            except Exception as e:
                self.logging.error(f"Unknown bug, more here: {e}")
        self.logging.info(f"Data collected: {self.site_path}")
        self.driver.quit()
        result_queue.put(self.events_data)


class STSThreeWayBets(STSScraper):
    def __init__(self, site_path: str) -> None:
        super().__init__(site_path)
        self.events_data = ThreeWayBetEventsTable("STS")

    def get_events_values(self, result_queue):
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
            except NoSuchElementException as e:
                pass
            except Exception as e:
                self.logging.error(f"Unknown bug, more here: {e}")
        self.logging.info(f"Data collected: {self.site_path}")
        self.driver.quit()
        result_queue.put(self.events_data)
