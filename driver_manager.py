"""Manager for the Selenium driver."""

from selenium import webdriver


class DriverManager:
    """Hold the current WebDriver and control when it starts and quits.

    The driver fixture calls start() before each test and quit() after it.
    Other code, such as page elements, reads the current browser from .driver.
    """

    def __init__(self):
        self.driver = None

    def start(self, headed=False):
        """Start a maximized WebDriver and make it the current driver.

        The browser runs headless unless headed is True. Returns the new
        driver, which is also stored as self.driver.
        """
        options = webdriver.ChromeOptions()
        # maximize, not fullscreen: macOS native fullscreen breaks ActionChains in headed runs
        # (see docs/decisions/0001-maximize-window.md)
        options.add_argument("--start-maximized")

        if not headed:
            options.add_argument("--headless=new")  # latest headless flag
            # headless has no real screen and defaults to 800x600, so give it one to fill
            options.add_argument("--screen-info={1920x1080}")

        self.driver = webdriver.Chrome(options=options)
        return self.driver

    def quit(self):
        """Quit the current driver and set self.driver back to None."""
        self.driver.quit()
        self.driver = None


# shared instance: the driver fixture starts and quits it; other code reads driver_manager.driver
driver_manager = DriverManager()
