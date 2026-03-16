from selenium.webdriver.common.by import By as by
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support import expected_conditions as EC

from driver_factory import driver_factory
from pages.the_internet.checkboxes import CheckboxesPage



def test_checkboxes():

    driver = driver_factory.get_driver()
    driver.get("https://the-internet.herokuapp.com")

    page = CheckboxesPage

    driver.find_element('xpath', '//a[text()="Checkboxes"]').click()

    box_1 = driver.find_element('xpath', page.checkbox1)
    box_2 = driver.find_element('xpath', page.checkbox2)

    assert not box_1.is_selected()
    assert box_2.is_selected()

    box_1.click()
    box_2.click()

    assert box_1.is_selected()
    assert not box_2.is_selected()

    driver.quit()
