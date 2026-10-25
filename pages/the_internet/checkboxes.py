from pages.the_internet.base import BasePage
from elements import Checkbox, Text


class CheckboxesPage(BasePage):

    header_text = Text(('xpath', '//h3'))
    checkbox1 = Checkbox(('xpath', '//input[following-sibling::text()[1][normalize-space()="checkbox 1"]]'))
    checkbox2 = Checkbox(('xpath', '//input[following-sibling::text()[1][normalize-space()="checkbox 2"]]'))
