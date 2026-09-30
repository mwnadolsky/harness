from selenium import webdriver


class DriverFactory:

    @staticmethod
    def get_driver(headed=False):
        """Return a Chrome WebDriver."""
        options = webdriver.ChromeOptions()
        options.add_argument("--start-fullscreen")

        if not headed:
            options.add_argument("--headless=new")  # latest headless flag
            # headless has no real screen and defaults to 800x600, so give it one to fill
            options.add_argument("--screen-info={1920x1080}")

        return webdriver.Chrome(options=options)


# Singleton instance for your test
driver_factory = DriverFactory()
