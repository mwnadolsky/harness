from selenium import webdriver
from selenium.webdriver.chrome.options import Options



class Driver_Manager:

    def __init__(self):
        self.options = Options()

    def start(self, headed=False):

        if headed == False: self.options.add_argument("--headless")

        return webdriver.Chrome(options=self.options)


driver_manager = Driver_Manager()
