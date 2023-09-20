from selenium import webdriver
from selenium.webdriver.common.by import By

class TwoWayBets:

    def __init__(self) -> None:
        self.driver = webdriver.Chrome()