from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from scrapers.base import Scraper
import time


class BetclicScraper(Scraper):
    def __init__(self, site_path: str) -> None:
        super().__init__(site_path)
        self.competition_boxes: list = []
        self.events_objects: dict = {}

    def close_cookie_msg(self):
        try:
            close_button = self.driver.find_element(
                By.XPATH, '//*[@id="popin_tc_privacy_button_2"]'
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
            boxes = self.driver.find_elements(
                By.XPATH,
                "/html/body/app-desktop/div[1]/div/bcdk-content-scroller/div/sports-all-offer/sports-events-list/bcdk-vertical-scroller/div/div[2]/div/div/div[*]",
            )
            for box in boxes:
                if (
                    box.get_attribute("class")
                    == "groupEvents ng-star-inserted"
                ):
                    self.competition_boxes.append(box)
        except NoSuchElementException as e:
            print(e)
        print(len(self.competition_boxes))

    def get_all_events_objects(self):
        for box in self.competition_boxes:
            for event in box.find_elements(
                By.XPATH, "./div[2]/sports-events-event[*]"
            ):
                self.events_objects[event] = box.find_element(
                    By.CLASS_NAME, "groupEvents_headTitle"
                ).text
        print(len(self.events_objects))

    def get_events_from_site(self):
        self.close_cookie_msg()
        self.get_whole_site()
        self.get_whole_site()
        self.get_segments()
        self.get_all_events_objects()
        # except Exception as e:
        #     print(e)


class BetclicTwoWayBets(BetclicScraper):
    def __init__(self, site_path: str) -> None:
        super().__init__(site_path)


    def get_events_values(self):
        self.get_events_from_site()
        # parser = FortunaParsers()
        for event, date in self.events_objects.items():
            try:
                home_name = event.find_element(
                    By.XPATH,
                    "./a/div/scoreboards-scoreboard/scoreboards-scoreboard-global/div/div[1]/div",
                ).text
                away_name = event.find_element(
                    By.XPATH,
                    "./a/div/scoreboards-scoreboard/scoreboards-scoreboard-global/div/div[3]/div",
                ).text
                home_team_win = event.find_element(
                    By.XPATH,
                    "./a/sports-events-event-markets-v2/sports-markets-default-v2/div/sports-selections-selection[1]/div[1]/span[2]",
                ).text
                away_team_win = event.find_element(
                    By.XPATH,
                    "./a/sports-events-event-markets-v2/sports-markets-default-v2/div/sports-selections-selection[2]/div[1]/span[2]",
                ).text
                event_date = date
            except Exception as e:
                print(e)


class BetclicThreeWayBets(BetclicScraper):
    def __init__(self, site_path: str) -> None:
        super().__init__(site_path)

    def get_events_values(self):
        self.get_events_from_site()
        # parser = FortunaParsers()
        for event, date in self.events_objects.items():
            try:
                home_name = event.find_element(
                    By.XPATH,
                    "./a/div/scoreboards-scoreboard/scoreboards-scoreboard-global/div/div[1]/div",
                ).text
                away_name = event.find_element(
                    By.XPATH,
                    "./a/div/scoreboards-scoreboard/scoreboards-scoreboard-global/div/div[3]/div",
                ).text
                home_team_win = event.find_element(
                    By.XPATH,
                    "./a/sports-events-event-markets-v2/sports-markets-default-v2/div/sports-selections-selection[1]/div/span[2]",
                ).text
                draw = event.find_element(
                    By.XPATH,
                    "./a/sports-events-event-markets-v2/sports-markets-default-v2/div/sports-selections-selection[2]/div/span[2]",
                ).text
                away_team_win = event.find_element(
                    By.XPATH,
                    "./a/sports-events-event-markets-v2/sports-markets-default-v2/div/sports-selections-selection[3]/div/span[2]",
                ).text
                event_date = date
            except Exception as e:
                print(e)
