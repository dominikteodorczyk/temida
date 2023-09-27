from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from scrapers.base import Scraper
import time
from utils.parsers import STSParsers


class STSScraper(Scraper):
    def __init__(self, site_path: str) -> None:
        super().__init__(site_path)
        self.competition_boxes: list = []
        self.events_objects: list = []

    def close_cookie_msg(self):
        try:
            close_button = self.driver.find_element(
                By.XPATH,
                '//*[@id="CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll"]',
            )
            close_button.click()
        except Exception as e:
            print("Can't close cookies msg:", e)

    def get_whole_site(self):
        while True:
            try:
                close_button = self.driver.find_element(
                    By.XPATH,
                    "/html/body/app-mweb/div/div/div/div[1]/div/div[2]/app-prematch/app-sport/div[2]/app-popular/div/app-show-more-container/app-show-more-progress-info/div/sts-shared-static-button/button/span/span[2]/span",
                )
                close_button.click()
                time.sleep(0.5)
            except:
                break

    def get_segments(self):
        try:
            self.competition_boxes = self.driver.find_elements(
                By.XPATH,
                "/html/body/app-mweb/div/div/div/div[1]/div/div[2]/app-prematch/app-sport/div[2]/app-popular/div/app-show-more-container/bb-leagues-wrapper/bb-league[*]",
            )
        except NoSuchElementException as e:
            print(e)

        print(len(self.competition_boxes))

    def get_all_events_objects(self):
        for box in self.competition_boxes:
            for event in box.find_elements(
                By.XPATH, "./div/div[2]/bb-match[*]"
            ):
                self.events_objects.append(event)
        print(len(self.events_objects))

    def get_events_from_site(self):
        try:
            self.close_cookie_msg()
            self.get_whole_site()
            self.get_segments()
            self.get_all_events_objects()
        except Exception as e:
            print(e)

class STSTwoWayBets(STSScraper):
    def __init__(self, site_path: str) -> None:
        super().__init__(site_path)
        self.get_events_from_site()

    def get_events_values(self):
        parser = STSParsers()
        i = 1
        for event in self.events_objects:
            try:
                home_player = event.find_element(
                    By.XPATH, "./div/div[2]/div[1]/a/bb-score/div/div/div/p[1]"
                ).text
                away_player = event.find_element(
                    By.XPATH, "./div/div[2]/div[1]/a/bb-score/div/div/div/p[2]"
                ).text
                home_team_win = event.find_element(
                    By.XPATH, "./div/div[2]/div[2]/bb-opportunity/div/div/bb-odd[1]/div/div/div[2]"
                ).text
                away_team_win = event.find_element(
                    By.XPATH, "./div/div[2]/div[2]/bb-opportunity/div/div/bb-odd[2]/div/div/div[2]"
                ).text
                event_date = event.find_element(
                    By.XPATH, "./div/div[1]/div[1]/a/bb-score-header/div/div/div/div/span[1]"
                ).text
                time.sleep(0.01)
            except Exception as e:
                pass  # TODO: logger


class STSThreeWayBets(STSScraper):
    def __init__(self, site_path: str) -> None:
        super().__init__(site_path)
        self.get_events_from_site()

    def get_events_values(self):
        parser = STSParsers()
        i = 1
        for event in self.events_objects:
            try:
                home_player = event.find_element(
                    By.XPATH, "./div/div[2]/div[1]/a/bb-score/div/div/div/p[1]"
                ).text
                away_player = event.find_element(
                    By.XPATH, "./div/div[2]/div[1]/a/bb-score/div/div/div/p[2]"
                ).text
                home_team_win = event.find_element(
                    By.XPATH, "./div/div[2]/div[2]/bb-opportunity/div/div/bb-odd[1]/div/div/div[2]"
                ).text
                draw = event.find_element(
                    By.XPATH, "./div/div[2]/div[2]/bb-opportunity/div/div/bb-odd[2]/div/div/div[2]"
                ).text
                away_team_win = event.find_element(
                    By.XPATH, "./div/div[2]/div[2]/bb-opportunity/div/div/bb-odd[3]/div/div/div[2]"
                ).text
                event_date = event.find_element(
                    By.XPATH, "./div/div[1]/div[1]/a/bb-score-header/div/div/div/div/span[1]"
                ).text
                time.sleep(0.01)
            except Exception as e:
                pass  # TODO: logger
