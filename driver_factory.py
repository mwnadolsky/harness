from selenium import webdriver

# Global variable for headless mode
HEADLESS = True


def set_headless(value: bool):
    """Set the global headless mode."""
    global HEADLESS
    HEADLESS = value


class DriverFactory:

    @staticmethod
    def get_driver(headless=None):
        """Return a Chrome WebDriver. Uses global HEADLESS if not specified."""
        if headless is None:
            headless = HEADLESS

        options = webdriver.ChromeOptions()
        options.add_argument("--start-fullscreen")

        if headless:
            options.add_argument("--headless=new")  # latest headless flag
            # headless has no real screen and defaults to 800x600, so give it one to fill
            options.add_argument("--screen-info={1920x1080}")

        return webdriver.Chrome(options=options)


# Singleton instance for your test
driver_factory = DriverFactory()
