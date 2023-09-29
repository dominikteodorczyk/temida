from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from scrapers.base import Scraper
import time

class SuperbetScraper(Scraper):
    def __init__(self, site_path: str) -> None:
        super().__init__(site_path)
        self.competition_boxes: list = []
        self.events_objects: list = []

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
            self.competition_boxes = self.driver.find_elements(
                By.XPATH,
                "/html/body/div[1]/div/div/div[1]/div/div[2]/div/div[3]/div/div/div/div/div[1]/div/div[*]",
            )
        except NoSuchElementException as e:
            print(e)
        print(len(self.competition_boxes))

    def get_all_events_objects(self):
        for box in self.competition_boxes:
            for event in box.find_elements(
                By.XPATH, "./div[*]"
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