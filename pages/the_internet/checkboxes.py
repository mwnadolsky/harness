from pages.the_internet.base import BasePage
from elements import Checkbox


class CheckboxesPage(BasePage):

    header = '//h3'
    checkbox1 = '//input[following-sibling::text()[1][normalize-space()="checkbox 1"]]'
    checkbox2 = '//input[following-sibling::text()[1][normalize-space()="checkbox 2"]]'

    cb1 = Checkbox(('xpath', checkbox1))
    cb2 = Checkbox(('xpath', checkbox2))
