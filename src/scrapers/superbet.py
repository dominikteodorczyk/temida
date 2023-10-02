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
        self.driver.execute_script("window.scrollTo(0, 0);")

    def get_segments(self):
        pass

    def get_events_from_site(self):
        self.close_cookie_msg()
        self.get_whole_site()
        self.get_whole_site()
        self.get_segments()
        # except Exception as e:
        #     print(e)

class SuperbetTwoWayBets(SuperbetScraper):
    def __init__(self, site_path: str) -> None:
        super().__init__(site_path)


    def get_events_values(self):
        self.get_events_from_site()
        height = self.driver.execute_script("return window.scrollY;")
        self.driver.execute_script("window.scrollTo(0, 0);")
        while True:
            elements = self.driver.find_elements(
                By.XPATH, '//*[contains(@id, "event-")]/div/div[1]')
            for element in elements:
                try:
                    home_name = element.find_element(
                    By.XPATH, './div[1]/div[2]/div[1]/span[1]').text
                    away_name = element.find_element(
                    By.XPATH, './div[1]/div[2]/div[1]/span[2]').text
                    if f'{home_name}{away_name}' in self.events_objects: pass
                    else:
                        home_team_win = element.find_element(
                            By.XPATH,
                            "./div[2]/div[2]/div/div[1]/button/span[4]/span[2]",
                        ).text
                        away_team_win = element.find_element(
                            By.XPATH,
                            "./div[2]/div[2]/div/div[2]/button/span[4]/span[2]",
                        ).text
                        event_date = element.find_element(
                            By.XPATH,
                            "./div[1]/div[1]/span[1]",
                        ).text
                        self.events_objects.append(f'{home_name}{away_name}')
                except Exception as e:
                    print(e)
            self.driver.execute_script(f"window.scrollTo(0, window.scrollY + {4000});")
            time.sleep(0.01)
            new_height = self.driver.execute_script("return window.scrollY;")
            if height == new_height:
                break
            height = new_height
        print(len(self.events_objects))

class SuperbetThreeWayBets(SuperbetScraper):
    def __init__(self, site_path: str) -> None:
        super().__init__(site_path)

    def get_events_values(self):
        self.get_events_from_site()
        height = self.driver.execute_script("return window.scrollY;")
        self.driver.execute_script("window.scrollTo(0, 0);")
        while True:
            elements = self.driver.find_elements(
                By.XPATH, '//*[contains(@id, "event-")]/div/div[1]')
            for element in elements:
                try:
                    home_name = element.find_element(
                    By.XPATH, './div[1]/div[2]/div[1]/span[1]').text
                    away_name = element.find_element(
                    By.XPATH, './div[1]/div[2]/div[1]/span[2]').text
                    if f'{home_name}{away_name}' in self.events_objects: pass
                    else:
                        home_team_win = element.find_element(
                            By.XPATH,
                            "./div[2]/div[2]/div/div[1]/button/span[4]/span[2]",
                        ).text
                        draw = element.find_element(
                            By.XPATH,
                            "./div[2]/div[2]/div/div[2]/button/span[4]/span[2]",
                        ).text
                        away_team_win = element.find_element(
                            By.XPATH,
                            "./div[2]/div[2]/div/div[3]/button/span[4]/span[2]",
                        ).text
                        event_date = element.find_element(
                            By.XPATH,
                            "./div[1]/div[1]/span[1]",
                        ).text
                        self.events_objects.append(f'{home_name}{away_name}')
                except Exception as e:
                    print(e)
            self.driver.execute_script(f"window.scrollTo(0, window.scrollY + {4000});")
            time.sleep(0.01)
            new_height = self.driver.execute_script("return window.scrollY;")
            if height == new_height:
                break
            height = new_height
        print(len(self.events_objects))
