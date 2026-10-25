"""Page object for the Dropdown page (/dropdown)."""

from pages.the_internet.base import BasePage
from elements import Dropdown, Text


class DropdownPage(BasePage):
    """Page object for the Dropdown page."""

    header_text = Text(('xpath', '//h3'))
    option_dropdown = Dropdown(('xpath', '//select[@id="dropdown"]'))
