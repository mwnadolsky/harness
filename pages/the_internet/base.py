"""Element objects shared by every standard page of the-internet."""

from elements import Link, Text


class BasePage:
    """Base class for the-internet page objects."""

    # flash-messages is always on the page, but flash only exists while a message is active
    flash_text = Text(('xpath', '//div[@id="flash-messages"]/div[@id="flash"]'))
    fork_me_on_github_link = Link(('xpath', '//a[img[@alt="Fork me on GitHub"]]'))
    elemental_selenium_link = Link(('xpath', '//div[@id="page-footer"]//a[text()="Elemental Selenium"]'))
