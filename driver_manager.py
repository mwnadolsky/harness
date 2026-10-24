from selenium import webdriver


class DriverManager:

    def __init__(self):
        self.driver = None

    def start(self, headed=False):
        """Start a Chrome WebDriver and keep it as the current driver."""
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
        """Quit the current driver."""
        self.driver.quit()
        self.driver = None


# shared instance: the driver fixture starts and quits it; other code reads driver_manager.driver
driver_manager = DriverManager()
