from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from scrapers.base import Scraper
import time


class BetclicScraper(Scraper):
    def __init__(self, site_path: str) -> None:
        super().__init__(site_path)
        self.competition_boxes: list = []
        self.events_objects: list = []

    def close_cookie_msg(self):
        pass
        #Betclicl dont have cookies msg box LOL

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
        print('Załadowano całą strone')

    def get_segments(self):
        try:
            boxes = self.driver.find_elements(
                By.XPATH, '/html/body/app-desktop/div[1]/div/bcdk-content-scroller/div/sports-all-offer/sports-events-list/bcdk-vertical-scroller/div/div[2]/div/div/div[*]'
            )
            for box in boxes:
                if box.get_attribute("class") == "groupEvents ng-star-inserted":
                    self.competition_boxes.append(box)
        except NoSuchElementException as e:
            print(e)
        print(len(self.competition_boxes))

    def get_all_events_objects(self):
        for box in self.competition_boxes:
            for event in box.find_elements(
                By.XPATH, "./div[2]/sports-events-event[*]"
            ):
                self.events_objects.append(event)
        print(len(self.events_objects))

    def get_events_from_site(self):
        self.close_cookie_msg()
        self.get_whole_site()
        self.get_whole_site()
        self.get_segments()
        self.get_all_events_objects()
        # except Exception as e:
        #     print(e)
