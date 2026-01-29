from selenium import webdriver
from selenium.webdriver.common.by import By as by
import random



def test_title():

    driver = webdriver.Chrome()
    driver.get("https://the-internet.herokuapp.com/")

    assert "The Internet" in driver.title

    driver.quit()

def test_search_home_page():
    driver = webdriver.Chrome()
    driver.get("https://the-internet.herokuapp.com/")

    list_container = driver.find_element(by.ID, "content")

    full_list_text = list_container.text
    lines = [line.strip() for line in full_list_text.split('\n') if line.strip()]

    #for this particular list taking the below lines out results in the complete intternet home page list
    home_page_list = [line for line in lines if line not in ["Welcome to the-internet", "Available Examples", "Powered by", "Elemental Selenium"]]

    random_search_term = random.choice(home_page_list)
    search_words = random_search_term.lower().split()

    link = driver.find_element('xpath', f'*//a[text()= "{random_search_term}"]')
    link.click()

    url_parts = driver.current_url.split('/')
    last_url_part = url_parts[-1]

    assert any(word in last_url_part for word in search_words)

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
