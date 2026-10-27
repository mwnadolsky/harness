import pytest
from pages.the_internet.add_remove_elements import AddRemoveElementsPage
from pages.the_internet.broken_images import BrokenImagesPage
from pages.the_internet.checkboxes import CheckboxesPage
from pages.the_internet.dropdown import DropdownPage
from pages.the_internet.home import HomePage

pytestmark = pytest.mark.regression_po


def test_add_elements(driver):

    page = HomePage

    page.add_remove_elements_link.click()

    page = AddRemoveElementsPage

    assert page.header_text.text == "Add/Remove Elements"
    assert page.delete_buttons.count() == 0

    page.add_element_button.click()

    assert page.delete_buttons.count() == 1

    page.add_element_button.click()

    assert page.delete_buttons.count() == 2


def test_remove_elements(driver):

    page = HomePage

    page.add_remove_elements_link.click()

    page = AddRemoveElementsPage

    page.add_element_button.click()

    assert page.delete_buttons.count() == 1

    page.delete_buttons.nth(0).click()

    assert page.delete_buttons.count() == 0


def test_broken_images(driver):

    page = HomePage

    page.broken_images_link.click()

    page = BrokenImagesPage

    assert page.header_text.text == "Broken Images"
    assert page.image_1_image.is_broken()
    assert page.image_2_image.is_broken()
    assert not page.image_3_image.is_broken()


@pytest.mark.smoke
def test_checkboxes(driver):

    page = HomePage

    page.checkboxes_link.click()

    page = CheckboxesPage

    assert page.header_text.text == "Checkboxes"
    assert not page.checkbox_1_checkbox.is_selected()
    assert page.checkbox_2_checkbox.is_selected()

    page.checkbox_1_checkbox.toggle()
    page.checkbox_2_checkbox.toggle()

    assert page.checkbox_1_checkbox.is_selected()
    assert not page.checkbox_2_checkbox.is_selected()


@pytest.mark.smoke
def test_dropdown(driver):

    page = HomePage

    page.dropdown_link.click()

    page = DropdownPage

    page.option_dropdown.click()
    page.option_dropdown.option("Option 1").click()

    assert page.option_dropdown.option("Option 1").is_selected()

    page.option_dropdown.click()
    page.option_dropdown.option("Option 2").click()

    assert page.option_dropdown.option("Option 2").is_selected()
