from selenium import webdriver
from selenium.webdriver.common.by import By as by
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

def test_elemental_selenium_link():

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
    driver = webdriver.Chrome()
    driver.get("https://the-internet.herokuapp.com/")
    time.sleep(1)
    link = driver.find_element('xpath', '//a[text()="Basic Auth"]')
    print("handle 0")
    print(driver.window_handles)
    time.sleep(1)
    link.click()
    time.sleep(5)
    """try:
        WebDriverWait(driver, 20).until(EC.alert_is_present())

        alert = driver.switch_to.alert
        alert.accept() # Or dismiss() or send_keys()
    except TimeoutException:
        print("No alert present within the given time.")
    except NoAlertPresentException:
        print("No alert present at this moment.")
    driver.switch_to.alert """

    #popup = WebDriverWait(driver, 10).until(
    #EC.presence_of_element_located((by.XPATH, "//div[@class='modal' or contains(@class,'popup')]")))
    #print(popup)

    print("popups")
    # Or find by CSS selecto
    """popup2 = driver.find_element(by.CSS_SELECTOR, ".modal, .popup, [role='dialog']")
    print(popup2)"""

    current_handle = driver.current_window_handle
    print("handles")
    print(str(current_handle))
    time.sleep(2)

    all_elements = driver.find_elements(by.XPATH, "//*")
    print(all_elements)

    print("handle 1")
    current_handle = driver.current_window_handle
    print(str(current_handle))
    print(driver.__getattribute__)
    print(driver.window_handles)
    print("handle 2")

    #WebDriverWait(driver, 10).until(EC.alert_is_present())
    #alert = driver.switch_to.alert
    #text = alert.text
    #print(text)

    #print(driver.switch_to.alert.text)
    print("handle 3")
    print(driver.window_handles)

    time.sleep(2)

    shadow_host = driver.find_element(by.CSS_SELECTOR, "css-selector-of-shadow-host")

# 2. Get the shadow root
    shadow_root = shadow_host.get_shadow_root()

# 3. Locate the element inside the shadow DOM
    inner_element = shadow_root.find_element(by.CSS_SELECTOR, "css-selector-inside-shadow-root")

    inner_element.click()

    all_elements = driver.find_elements(by.XPATH, "//*")
    print(all_elements)

    # get the first line of text on the page
    page_text = driver.find_element(by.TAG_NAME, 'body').text
    #first_line = next(line for line in page_text.splitlines() if line.strip())
    print("handle 4")
    print(page_text)

    #assert first_line == 'Basic Auth'



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
    print("does this work")

    driver.quit()
