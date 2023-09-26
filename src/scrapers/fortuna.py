from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from scrapers.base import Scraper
import time
from utils.parsers import FortunaParsers


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
            time.sleep(2)
            new_height = self.driver.execute_script(
                "return document.body.scrollHeight"
            )
            if new_height == last_height:
                break
            last_height = new_height
        time.sleep(5)

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
        print(len(self.events_objects))

    def get_events_from_site(self):
        try:
            self.close_cookie_msg()
            self.get_whole_site()
            self.get_segments()
            self.get_all_events_objects()
        except Exception as e:
            print(e)


class FortunaTwoWayBets(FortunaScraper):
    def __init__(self, site_path: str) -> None:
        super().__init__(site_path)
        self.get_events_from_site()

    def get_events_values(self):
        parser = FortunaParsers()
        i = 1
        for event in self.events_objects:
            try:
                event_name = event.find_element(
                    By.XPATH, ".//td[1]/div/div[1]/span[1]"
                ).text
                home_team_win = event.find_element(
                    By.XPATH, ".//td[2]/a/span"
                ).text
                away_team_win = event.find_element(
                    By.XPATH, ".//td[3]/a/span"
                ).text
                event_date = event.find_element(
                    By.CLASS_NAME, "event-datetime"
                ).text
                time.sleep(0.01)
            except Exception as e:
                pass  # TODO: logger

            i += 1


class FortunaThreeWayBets(FortunaScraper):
    def __init__(self, site_path: str) -> None:
        super().__init__(site_path)
        self.get_events_from_site()

    def get_events_values(self):
        parser = FortunaParsers()
        i = 1
        for event in self.events_objects:
            try:
                event_name = event.find_element(
                    By.XPATH, ".//td[1]/div/div[1]/span[1]"
                ).text
                home_team_win = event.find_element(
                    By.XPATH, ".//td[2]/a/span"
                ).text
                draw = event.find_element(By.XPATH, ".//td[3]/a/span").text
                away_team_win = event.find_element(
                    By.XPATH, ".//td[4]/a/span"
                ).text
                event_date = event.find_element(
                    By.CLASS_NAME, "event-datetime"
                ).text
                time.sleep(0.01)
            except Exception as e:
                # print(event_name,e)TODO: logger
                pass

            i += 1
