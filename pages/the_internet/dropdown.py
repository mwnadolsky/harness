from pages.the_internet.base import BasePage


class DropdownPage(BasePage):

    header = '//h3'
    dropdown = '//select[@id="dropdown"]'
    option1 = '//option[text()="Option 1"]'
    option2 = '//option[text()="Option 2"]'
