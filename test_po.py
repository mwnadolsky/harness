import pytest
from pages.the_internet.checkboxes import CheckboxesPage
from pages.the_internet.dropdown import DropdownPage
from pages.the_internet.home import HomePage

pytestmark = pytest.mark.regression_po


@pytest.mark.smoke
def test_checkboxes(driver):

    driver.get("https://the-internet.herokuapp.com")

    page = CheckboxesPage

    HomePage.checkboxes_link.click()

    assert page.header_text.text == "Checkboxes"
    assert not page.checkbox1.is_selected()
    assert page.checkbox2.is_selected()

    page.checkbox1.toggle()
    page.checkbox2.toggle()

    assert page.checkbox1.is_selected()
    assert not page.checkbox2.is_selected()


@pytest.mark.smoke
def test_dropdown(driver):

    driver.get("https://the-internet.herokuapp.com/")

    page = DropdownPage

    HomePage.dropdown_link.click()

    dropdown = driver.find_element('xpath', page.dropdown)
    option_1 = driver.find_element('xpath', page.option1)
    option_2 = driver.find_element('xpath', page.option2)

    dropdown.click()
    option_1.click()

    assert option_1.is_selected()

    dropdown.click()
    option_2.click()

    assert option_2.is_selected()
