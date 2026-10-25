import pytest
from pages.the_internet.checkboxes import CheckboxesPage
from pages.the_internet.dropdown import DropdownPage
from pages.the_internet.home import HomePage

pytestmark = pytest.mark.regression_po


@pytest.mark.smoke
def test_checkboxes(driver):

    driver.get("https://the-internet.herokuapp.com")

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

    driver.get("https://the-internet.herokuapp.com/")

    page = HomePage

    page.dropdown_link.click()

    page = DropdownPage

    page.dropdown_dropdown.click()
    page.dropdown_dropdown.option("Option 1").click()

    assert page.dropdown_dropdown.option("Option 1").is_selected()

    page.dropdown_dropdown.click()
    page.dropdown_dropdown.option("Option 2").click()

    assert page.dropdown_dropdown.option("Option 2").is_selected()
