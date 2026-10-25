"""Page object for the Checkboxes page (/checkboxes)."""

from pages.the_internet.base import BasePage
from elements import Checkbox, Text


class CheckboxesPage(BasePage):
    """The Checkboxes page: a heading and two checkboxes."""

    header_text = Text(('xpath', '//h3'))
    checkbox_1_checkbox = Checkbox(('xpath', '//input[following-sibling::text()[1][normalize-space()="checkbox 1"]]'))
    checkbox_2_checkbox = Checkbox(('xpath', '//input[following-sibling::text()[1][normalize-space()="checkbox 2"]]'))
