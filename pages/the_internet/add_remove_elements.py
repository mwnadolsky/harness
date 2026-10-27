"""Page object for the Add/Remove Elements page (/add_remove_elements/)."""

from pages.the_internet.base import BasePage
from elements import Button, Text


class AddRemoveElementsPage(BasePage):
    """Page object for the Add/Remove Elements page."""

    header_text = Text(('xpath', '//h3'))
    add_element_button = Button(('xpath', '//button[text()="Add Element"]'))
    # one Delete button per added element
    delete_buttons = Button(('xpath', '//div[@id="elements"]/button[text()="Delete"]'))
