from selenium import webdriver
from selenium.webdriver.common.by import By as by
from selenium import EC
import random
import pytest
import time



def test_title():

    driver = webdriver.Chrome()
    driver.get("https://the-internet.herokuapp.com/")

    assert "The Internet" in driver.title

    driver.quit()

def test_ab_testing():

    driver = webdriver.Chrome()
    driver.get("https://the-internet.herokuapp.com/")

    link = driver.find_element('xpath', '//a[text()="A/B Testing"]')
    link.click()

    # get the first line of text on the page
    page_text = driver.find_element(by.TAG_NAME, 'body').text
    first_line = next(line for line in page_text.splitlines() if line.strip())
    
    assert first_line == 'A/B Test Variation 1' or first_line == 'A/B Test Control'

    driver.quit()

def test_ab_testing_elemental_selenium_link():

    driver = webdriver.Chrome()
    driver.get("https://the-internet.herokuapp.com/")

    link = driver.find_element('xpath', '//a[text()="A/B Testing"]')
    link.click()

    link = driver.find_element('xpath','//a[text()="Elemental Selenium"]')
    link.click()

    driver.switch_to.window(driver.window_handles[1])

    assert "Elemental Selenium" in driver.title 

    driver.quit()


def test_add_elements():

    driver = webdriver.Chrome()
    driver.get("https://the-internet.herokuapp.com/")

    driver.find_element('xpath', '//a[text()="Add/Remove Elements"]').click()

    buttons = driver.find_elements('xpath', '//button[@class="added-manually"]')

    assert len(buttons) == 0

    add_element_button = driver.find_element('xpath', '//button[text()="Add Element"]')
    add_element_button.click()
    buttons = driver.find_elements('xpath', '//button[@class="added-manually"]')

    assert len(buttons) == 1

    add_element_button.click()
    buttons = driver.find_elements('xpath', '//button[@class="added-manually"]')

    assert len(buttons) == 2

    driver.quit()


def test_remove_elements():

    driver = webdriver.Chrome()
    driver.get("https://the-internet.herokuapp.com/")

    driver.find_element('xpath', '//a[text()="Add/Remove Elements"]').click()

    driver.find_element('xpath', '//button[text()="Add Element"]').click()

    buttons = driver.find_elements('xpath', '//button[@class="added-manually"]')

    assert len(buttons) == 1

    driver.find_element('xpath', '//button[text()="Delete"]').click()

    buttons = driver.find_elements('xpath', '//button[@class="added-manually"]')

    assert len(buttons) == 0

    driver.quit()


def test_basic_auth_login():

    driver = webdriver.Chrome()
    driver.get("https://admin:admin@the-internet.herokuapp.com/basic_auth")

    # get the first line of text on the page
    page_text = driver.find_element(by.TAG_NAME, 'body').text
    first_line = next(line for line in page_text.splitlines() if line.strip())

    assert first_line == 'Basic Auth'

def test_challenging_dom_three_buttons():

    driver = webdriver.Chrome()
    driver.get("https://the-internet.herokuapp.com/")
    driver.find_element('xpath', '//a[text()="Challenging DOM"]').click()

    #This test is to verify that the text on the three buttons are different after clicking the top button
    #A thorough test would be repeated for the remaining two buttons.    
    
    button_text1_b = driver.find_element('xpath', '//a[contains(@class, "button")]').text
    button_text2_b = driver.find_element('xpath', '//a[contains(@class, "button alert")]').text
    button_text3_b = driver.find_element('xpath', '//a[contains(@class, "button success")]').text

    driver.find_element('xpath', '//a[contains(@class, "button")]').click()

    button_text1_a = driver.find_element('xpath', '//a[contains(@class, "button")]').text
    button_text2_a = driver.find_element('xpath', '//a[contains(@class, "button alert")]').text
    button_text3_a = driver.find_element('xpath', '//a[contains(@class, "button success")]').text

    def are_button_texts_different(string1, string2, string3):
        return string1 != string2 or string1 != string3 or string2 != string3

    assert are_button_texts_different(button_text1_a, button_text2_a, button_text3_a), "after clicking the top button all of the buttons texts are the same"

    #This test is to verify that the text on the three buttons before the button is clicked changes after the button is clicked

    text_before_click = [button_text1_b, button_text2_b, button_text3_b]
    text_after_click = [button_text1_a, button_text2_a, button_text3_a]

    assert text_before_click != text_after_click, "the buttons texts before clicking the top button matches the text after clicking it"

    driver.quit()


def test_challenging_dom_edit_delete_links():

    driver = webdriver.Chrome()

    edit_link_loc_1 = (by.XPATH, "(//a[text()='edit'])[1]")

    element = EC.presence_of_element_located((edit_link_loc_1))(driver)
    print(element)

    driver.quit()

def test_checkboxes():

    driver = webdriver.Chrome()
    driver.get("https://admin:admin@the-internet.herokuapp.com")

    driver.find_element('xpath', '//a[text()="Checkboxes"]').click()

    box_1 = driver.find_element('xpath', '//input[@type="checkbox" and normalize-space(following-sibling::text()[1])="checkbox 1"]')
    box_2 = driver.find_element('xpath', '//input[@type="checkbox" and normalize-space(following-sibling::text()[1])="checkbox 2"]')

    assert not box_1.is_selected()
    assert box_2.is_selected()

    box_1.click()
    box_2.click()

    assert box_1.is_selected()
    assert not box_2.is_selected()

    driver.quit()
