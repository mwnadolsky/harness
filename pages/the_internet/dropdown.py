"""Page object for the Dropdown page (/dropdown)."""

from pages.the_internet.base import BasePage


class DropdownPage(BasePage):
    """The Dropdown page: a heading and a dropdown with two options."""

    header = '//h3'
    dropdown = '//select[@id="dropdown"]'
    option1 = '//option[text()="Option 1"]'
    option2 = '//option[text()="Option 2"]'
