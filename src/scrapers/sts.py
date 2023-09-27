from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from scrapers.base import Scraper
import time


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
