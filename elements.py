from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC

from driver_manager import driver_manager


class BaseElement:

    def __init__(self, locator):
        self.locator = locator

    def element(self):

        wait(driver_manager.driver, 10).until(
            EC.presence_of_element_located(self.locator))
        return driver_manager.driver.find_element(*self.locator)

    # only called for names the element class doesn't define; hands them to the Selenium element
    # (e.g. click, is_selected, text)
    def __getattr__(self, name):
        # never delegate dunder names: Python and tools (copy, pickle, debuggers) probe for them,
        # and delegating would hit the browser or recurse forever on half-built objects
        if name.startswith("__") and name.endswith("__"):
            raise AttributeError(name)
        return getattr(self.element(), name)


class Checkbox(BaseElement):

    def toggle(self):

        wait(driver_manager.driver, 10).until(EC.element_to_be_clickable(self.locator))
        self.element().click()


class Link(BaseElement):
    pass


class Text(BaseElement):
    pass
