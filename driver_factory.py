from selenium import webdriver


class DriverFactory:

    @staticmethod
    def get_driver(headed=False):
        """Return a Chrome WebDriver."""
        options = webdriver.ChromeOptions()

        if not headed:
            options.add_argument("--headless=new")  # latest headless flag
            # headless has no real screen and defaults to 800x600, so give it one to fill
            options.add_argument("--screen-info={1920x1080}")

        driver = webdriver.Chrome(options=options)
        # maximize, not fullscreen: macOS native fullscreen breaks ActionChains in headed runs
        # (see docs/decisions/0001-maximize-window.md)
        driver.maximize_window()

        return driver


# Singleton instance for your test
driver_factory = DriverFactory()
