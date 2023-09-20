from selenium import webdriver
from selenium.webdriver.common.by import By

class TwoWayBets:

    def __init__(self, site_path:str) -> None:
        self.driver = webdriver.Chrome()
        self.driver.get(site_path)

# //*[@id="sport-events-list-content"]/section[2]/div[2]/div/div/table/tbody/tr[3]/td[1]/div/div[1]/span[1]
# //*[@id="sport-events-list-content"]/section[2]/div[2]/div/div/table/tbody/tr[3]/td[2]/a/span
# //*[@id="sport-events-list-content"]/section[2]/div[2]/div/div/table/tbody/tr[3]/td[3]/a/span


# //*[@id="sport-events-list-content"]/section[3]/div[2]/div/div/table/tbody/tr[1]/td[1]/div/div[1]/span[1]
# //*[@id="sport-events-list-content"]/section[3]/div[2]/div/div/table/tbody/tr[1]/td[2]/a/span
# //*[@id="sport-events-list-content"]/section[3]/div[2]/div/div/table/tbody/tr[1]/td[3]/a/span


# //*[@id="sport-events-list-content"]/section[2]/div[2]/div/div/table/tbody