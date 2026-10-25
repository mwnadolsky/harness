"""Locators shared by every standard page of the-internet."""


class BasePage:
    """Base class for the-internet page objects: what every standard page shows."""

    # flash-messages is always on the page, but flash only exists while a message is active
    flash = '//div[@id="flash-messages"]/div[@id="flash"]'
    fork_me_on_github = '//a[img[@alt="Fork me on GitHub"]]'
    elemental_selenium = '//div[@id="page-footer"]//a[text()="Elemental Selenium"]'
