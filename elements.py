from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC

from driver_manager import driver_manager


class Checkbox:

    def __init__(self, locator):
        self.locator = locator

    def element(self):

        wait(driver_manager.driver, 10).until(
            EC.presence_of_element_located(self.locator))
        return driver_manager.driver.find_element(*self.locator)

    def toggle(self):

        wait(driver_manager.driver, 10).until(EC.element_to_be_clickable(self.locator))
        self.element().click()

    # only called for names Checkbox doesn't define; hands them to the Selenium element
    # (e.g. click, is_selected, text)
    def __getattr__(self, name):
        return getattr(self.element(), name)
