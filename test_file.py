from selenium import webdriver
from selenium.webdriver.common.by import By as by
from selenium.webdriver.support import expected_conditions as EC
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

    driver.get("https://the-internet.herokuapp.com/")
    driver.find_element('xpath', '//a[text()="Challenging DOM"]').click()

    edit_link_loc_1 = (by.XPATH, "(//a[text()='edit'])[1]")
    edit_link_loc_2 = (by.XPATH, "(//a[text()='edit'])[2]")
    edit_link_loc_3 = (by.XPATH, "(//a[text()='edit'])[3]")
    edit_link_loc_4 = (by.XPATH, "(//a[text()='edit'])[4]")
    edit_link_loc_5 = (by.XPATH, "(//a[text()='edit'])[5]")
    edit_link_loc_6 = (by.XPATH, "(//a[text()='edit'])[6]")
    edit_link_loc_7 = (by.XPATH, "(//a[text()='edit'])[7]")
    edit_link_loc_8 = (by.XPATH, "(//a[text()='edit'])[8]")
    edit_link_loc_9 = (by.XPATH, "(//a[text()='edit'])[9]")
    edit_link_loc_10 = (by.XPATH, "(//a[text()='edit'])[10]")

    edit_element_1 = EC.element_to_be_clickable((edit_link_loc_1))(driver)
    edit_element_2 = EC.element_to_be_clickable((edit_link_loc_2))(driver)
    edit_element_3 = EC.element_to_be_clickable((edit_link_loc_3))(driver)
    edit_element_4 = EC.element_to_be_clickable((edit_link_loc_4))(driver)
    edit_element_5 = EC.element_to_be_clickable((edit_link_loc_5))(driver)
    edit_element_6 = EC.element_to_be_clickable((edit_link_loc_6))(driver)
    edit_element_7 = EC.element_to_be_clickable((edit_link_loc_7))(driver)
    edit_element_8 = EC.element_to_be_clickable((edit_link_loc_8))(driver)
    edit_element_9 = EC.element_to_be_clickable((edit_link_loc_9))(driver)
    edit_element_10 = EC.element_to_be_clickable((edit_link_loc_10))(driver)

    assert bool(edit_element_1)
    assert bool(edit_element_2)
    assert bool(edit_element_3)
    assert bool(edit_element_4)
    assert bool(edit_element_5)
    assert bool(edit_element_6)
    assert bool(edit_element_7)
    assert bool(edit_element_8)
    assert bool(edit_element_9)
    assert bool(edit_element_10)

    delete_link_loc_1 = (by.XPATH, "(//a[text()='delete'])[1]")
    delete_link_loc_2 = (by.XPATH, "(//a[text()='delete'])[2]")
    delete_link_loc_3 = (by.XPATH, "(//a[text()='delete'])[3]")
    delete_link_loc_4 = (by.XPATH, "(//a[text()='delete'])[4]")
    delete_link_loc_5 = (by.XPATH, "(//a[text()='delete'])[5]")
    delete_link_loc_6 = (by.XPATH, "(//a[text()='delete'])[6]")
    delete_link_loc_7 = (by.XPATH, "(//a[text()='delete'])[7]")
    delete_link_loc_8 = (by.XPATH, "(//a[text()='delete'])[8]")
    delete_link_loc_9 = (by.XPATH, "(//a[text()='delete'])[9]")
    delete_link_loc_10 = (by.XPATH, "(//a[text()='delete'])[10]")

    delete_element_1 = EC.element_to_be_clickable((delete_link_loc_1))(driver)
    delete_element_2 = EC.element_to_be_clickable((delete_link_loc_2))(driver)
    delete_element_3 = EC.element_to_be_clickable((delete_link_loc_3))(driver)
    delete_element_4 = EC.element_to_be_clickable((delete_link_loc_4))(driver)
    delete_element_5 = EC.element_to_be_clickable((delete_link_loc_5))(driver)
    delete_element_6 = EC.element_to_be_clickable((delete_link_loc_6))(driver)
    delete_element_7 = EC.element_to_be_clickable((delete_link_loc_7))(driver)
    delete_element_8 = EC.element_to_be_clickable((delete_link_loc_8))(driver)
    delete_element_9 = EC.element_to_be_clickable((delete_link_loc_9))(driver)
    delete_element_10 = EC.element_to_be_clickable((delete_link_loc_10))(driver)

    assert bool(delete_element_1)
    assert bool(delete_element_2)
    assert bool(delete_element_3)
    assert bool(delete_element_4)
    assert bool(delete_element_5)
    assert bool(delete_element_6)
    assert bool(delete_element_7)
    assert bool(delete_element_8)
    assert bool(delete_element_9)
    assert bool(delete_element_10)

    driver.quit()


def test_challenging_dom_table_data():
    driver = webdriver.Chrome()
    driver.get("https://the-internet.herokuapp.com/")
    driver.find_element('xpath', '//a[text()="Challenging DOM"]').click()



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
