from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from scrapers.base import Scraper
import time

class SuperbetScraper(Scraper):
    def __init__(self, site_path: str) -> None:
        super().__init__(site_path)
        self.competition_boxes: list = []
        self.events_objects: dict = {}

    def close_cookie_msg(self):
        try:
            close_button = self.driver.find_element(
                By.XPATH, '//*[@id="onetrust-accept-btn-handler"]'
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
            self.driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(10)

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

//*[@id="S-106"]

    def get_events_from_site(self):
        self.close_cookie_msg()
        self.get_whole_site()
        # self.get_whole_site()
        # self.get_segments()
        # self.get_all_events_objects()
        # except Exception as e:
        #     print(e)