from selenium import webdriver
from selenium.common.exceptions import SessionNotCreatedException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait


class Scraper:

    def __init__(self, site_path:object) -> None:
        options = Options()
        options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(options=options)
        try:
            self.driver.get(site_path)
        except SessionNotCreatedException as e:
            print(e)

        self.wait = WebDriverWait(self.driver, 20)