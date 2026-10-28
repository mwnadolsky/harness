import pytest
from pages.the_internet.abtest import AbtestPage
from pages.the_internet.add_remove_elements import AddRemoveElementsPage
from pages.the_internet.broken_images import BrokenImagesPage
from pages.the_internet.checkboxes import CheckboxesPage
from pages.the_internet.dropdown import DropdownPage
from pages.the_internet.home import HomePage

pytestmark = pytest.mark.regression_po


def test_ab_testing_sticky(driver):

    page = HomePage()

    page.ab_testing_link.click()

    page = AbtestPage()

    variant = page.header_text.text

    assert variant in ("A/B Test Control", "A/B Test Variation 1")

    for _ in range(5):
        driver.refresh()

        assert page.header_text.text == variant


def test_ab_testing_variants(driver):

    page = HomePage()

    page.ab_testing_link.click()

    page = AbtestPage()

    variants = {"A/B Test Control", "A/B Test Variation 1"}
    seen = set()

    # each try is a new visitor: clearing the cookies drops the assigned variant.
    # 20 tries: with a 50/50 split, all 20 landing on one variant is a 1 in 524,288 chance
    for _ in range(20):
        driver.delete_all_cookies()
        driver.refresh()
        seen.add(page.header_text.text)
        if seen == variants:
            break

    assert seen == variants


def test_add_elements(driver):

    page = HomePage()

    page.add_remove_elements_link.click()

    page = AddRemoveElementsPage()

    assert page.header_text.text == "Add/Remove Elements"
    assert page.delete_buttons.count() == 0

    page.add_element_button.click()

    assert page.delete_buttons.count() == 1

    page.add_element_button.click()

    assert page.delete_buttons.count() == 2


def test_remove_elements(driver):

    page = HomePage()

    page.add_remove_elements_link.click()

    page = AddRemoveElementsPage()

    for _ in range(5):
        page.add_element_button.click()

    assert page.delete_buttons.count() == 5

    for remaining in reversed(range(5)):
        page.delete_buttons.random().click()

        assert page.delete_buttons.count() == remaining


def test_broken_images(driver):

    page = HomePage()

    page.broken_images_link.click()

    page = BrokenImagesPage()

    assert page.header_text.text == "Broken Images"
    assert page.image_1_image.is_broken()
    assert page.image_2_image.is_broken()
    assert not page.image_3_image.is_broken()


@pytest.mark.smoke
def test_checkboxes(driver):

    page = HomePage()

    page.checkboxes_link.click()

    page = CheckboxesPage()

    assert page.header_text.text == "Checkboxes"
    assert not page.checkbox_1_checkbox.is_selected()
    assert page.checkbox_2_checkbox.is_selected()

    page.checkbox_1_checkbox.toggle()
    page.checkbox_2_checkbox.toggle()

    assert page.checkbox_1_checkbox.is_selected()
    assert not page.checkbox_2_checkbox.is_selected()


@pytest.mark.smoke
def test_dropdown(driver):

    page = HomePage()

    page.dropdown_link.click()

    page = DropdownPage()

    page.option_dropdown.click()
    page.option_dropdown.option("Option 1").click()

    assert page.option_dropdown.option("Option 1").is_selected()

    page.option_dropdown.click()
    page.option_dropdown.option("Option 2").click()

    assert page.option_dropdown.option("Option 2").is_selected()
