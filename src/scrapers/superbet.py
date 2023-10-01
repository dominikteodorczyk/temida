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

class SuperbetScraper(Scraper):
    def __init__(self, site_path: str) -> None:
        super().__init__(site_path)
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
        self.driver.execute_script("window.scrollTo(0, 0);")

    def get_segments(self):
        pass

    def get_all_events_objects(self):
        height = self.driver.execute_script("return window.scrollY;")
        self.driver.execute_script("window.scrollTo(0, 0);")
        all_elements = []
        while True:
            elements = self.driver.find_elements(
                By.XPATH, '//*[contains(@id, "event-")]/div/div[1]')
            for element in elements:
                home = element.find_element(
                By.XPATH, './div[1]/div[2]/div[1]/span[1]').text
                away = element.find_element(
                By.XPATH, './div[1]/div[2]/div[1]/span[2]').text
                self.events_objects[f'{home}{away}'] = element
            self.driver.execute_script(f"window.scrollTo(0, window.scrollY + {4000});")
            time.sleep(0.2)
            new_height = self.driver.execute_script("return window.scrollY;")
            if height == new_height:
                break
            height = new_height
        print(len(self.events_objects))

    def get_events_from_site(self):
        self.close_cookie_msg()
        self.get_whole_site()
        self.get_whole_site()
        self.get_segments()
        self.get_all_events_objects()
        # except Exception as e:
        #     print(e)


