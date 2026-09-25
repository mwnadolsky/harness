from pages.the_internet.base import BasePage


class CheckboxesPage(BasePage):

    header = '//h3'
    checkbox1 = '//input[following-sibling::text()[1][normalize-space()="checkbox 1"]]'
    checkbox2 = '//input[following-sibling::text()[1][normalize-space()="checkbox 2"]]'
