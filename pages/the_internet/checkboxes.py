from pages.the_internet.base import BasePage
from elements import Checkbox


class CheckboxesPage(BasePage):

    header = '//h3'
    checkbox1 = Checkbox(('xpath', '//input[following-sibling::text()[1][normalize-space()="checkbox 1"]]'))
    checkbox2 = Checkbox(('xpath', '//input[following-sibling::text()[1][normalize-space()="checkbox 2"]]'))
