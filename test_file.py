from selenium import webdriver
from selenium.webdriver.common.by import By as by
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


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

    driver.quit()


def test_broken_images():

    driver = webdriver.Chrome()
    driver.get("https://the-internet.herokuapp.com/")
    driver.find_element('xpath', '//a[text()="Broken Images"]').click()

    images = driver.find_elements(by.TAG_NAME, 'img')

    broken_count = 0
    for img in images:
        # With Javascript I can see if the natural width is 0 and is therefore broken
        natural_width = driver.execute_script("return arguments[0].naturalWidth", img)

        if natural_width == 0:
            broken_count += 1

    assert 2 == broken_count

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

def test_dropdown():

    driver = webdriver.Chrome()
    driver.get("https://the-internet.herokuapp.com/")

    driver.find_element('xpath', '//a[text()="Dropdown"]').click()

    #find the dropdown
    dropdown = driver.find_element('xpath', '//select[@id="dropdown"]')
    dropdown.click()

    #pick option 1
    option_1 = driver.find_element('xpath', '//option[text()="Option 1"]')
    option_2 = driver.find_element('xpath', '//option[text()="Option 2"]')

    option_1.click()

    assert option_1.is_selected()

    #pick option 2
    dropdown.click()

    option_2.click()

    assert option_2.is_selected()

    driver.quit()
    
def test_context_menu():
  
    driver = webdriver.Chrome()
    driver.get("https://the-internet.herokuapp.com/")

    driver.find_element('xpath', '//a[text()="Context Menu"]').click()

    hot_spot = driver.find_element("xpath", '//div[@id="hot-spot"]')
    ActionChains(driver).context_click(hot_spot).perform()

    alert = driver.switch_to.alert
    alert_text = alert.text

    assert alert_text == 'You selected a context menu'

    alert.accept()
    
    driver.quit()


def test_slider():

    driver = webdriver.Chrome()    
    driver.get("https://the-internet.herokuapp.com/")
    
    actions = ActionChains(driver)
        
    driver.find_element('xpath', '//a[text()="Horizontal Slider"]').click()
    
    # Slider starts at 0
    display_value = driver.find_element('xpath', '//span[@id="range"]')
    assert display_value.text == "0"
    
    # Click on middle
    slider = driver.find_element('xpath', '//input[@type="range"]')
    slider.click()
    width = slider.size['width']
    assert display_value.text == "2.5"

    # Click on right side
    actions.move_to_element_with_offset(slider, width/2, 0).click().perform()
    assert display_value.text == "5"

    # Click on left side
    actions.move_by_offset(-width+1,0).click().perform()
    assert display_value.text == "0"

    # Click and drag right 80%
    actions.click_and_hold().move_by_offset(width*.8,0).release().perform()
    assert display_value.text == "4"

    # Click and drag left 40%
    actions.click_and_hold().move_by_offset(-width*.4,0).release().perform()
    assert display_value.text == "2"

    driver.quit()


def test_drag_and_drop():

    driver = webdriver.Chrome()     
    driver.get("https://the-internet.herokuapp.com/")
    
    actions = ActionChains(driver)
    
    driver.find_element('xpath', '//a[text()="Drag and Drop"]').click()

    # Identify boxes, confirm correct starting order
    left_box = driver.find_element('xpath', '//div[@id="column-a"]')
    right_box = driver.find_element('xpath', '//div[@id="column-b"]')
    assert left_box.text == "A" and right_box.text == "B"
    
    # Drag left box to right box, verify
    actions.drag_and_drop(left_box, right_box).perform()
    assert left_box.text == "B" and right_box.text == "A"

    # Drag right box to left box, verify
    actions.drag_and_drop(right_box, left_box).perform()
    assert left_box.text == "A" and right_box.text == "B"

    # Drag left box elsewhere, verify no change
    selenium_link = driver.find_element('xpath','//a[text()="Elemental Selenium"]')
    actions.drag_and_drop(left_box, selenium_link).perform()
    assert left_box.text == "A" and right_box.text == "B"

    driver.quit()


def test_js_alerts():

    driver = webdriver.Chrome()     
    driver.get("https://the-internet.herokuapp.com/")
    
    alert = Alert(driver)
    
    driver.find_element('xpath', '//a[text()="JavaScript Alerts"]').click()

    # First Button
    driver.find_element('xpath', '//button[text()="Click for JS Alert"]').click()
    alert.accept()
    result = driver.find_element('xpath', '//p[@id="result"]')
    assert result.text == "You successfully clicked an alert"
    
    # Second Button
    driver.find_element('xpath', '//button[text()="Click for JS Confirm"]').click()
    alert.accept()
    assert result.text == "You clicked: Ok"
    driver.find_element('xpath', '//button[text()="Click for JS Confirm"]').click()
    alert.dismiss()
    assert result.text == "You clicked: Cancel"

    # Third Button
    driver.find_element('xpath', '//button[text()="Click for JS Prompt"]').click() 
    alert.send_keys('Test')
    alert.accept()
    assert result.text == "You entered: Test"
    driver.find_element('xpath', '//button[text()="Click for JS Prompt"]').click() 
    alert.send_keys('Test')
    alert.dismiss()
    assert result.text == "You entered: null"

    driver.quit()


def test_form_auth():
    driver = webdriver.Chrome()     
    driver.get("https://the-internet.herokuapp.com/")
    
    driver.find_element('xpath', '//a[text()="Form Authentication"]').click()

    driver.execute_script('document.getElementById("username").value="tomsmith"')
    driver.execute_script('document.getElementById("password").value="SuperSecretPassword!";')
    driver.find_element('xpath','//button').click()
    
    assert driver.current_url == "https://the-internet.herokuapp.com/secure"
    
    driver.quit()


def test_form_auth_errors():

    driver = webdriver.Chrome()     
    driver.get("https://the-internet.herokuapp.com/")
    
    driver.find_element('xpath', '//a[text()="Form Authentication"]').click()

    # Both Blank
    driver.find_element('xpath','//button').click()
    WebDriverWait(driver, 2).until(EC.presence_of_element_located((by.ID, 'flash')))
    assert 'username' in driver.find_element(by.ID, "flash").text

    # Correct username, Blank password
    driver.execute_script('document.getElementById("username").value="tomsmith"')
    driver.find_element('xpath','//button').click()
    WebDriverWait(driver, 2).until(EC.presence_of_element_located((by.ID, 'flash')))
    assert 'password' in driver.find_element(by.ID, "flash").text

    # Blank username, Correct password
    driver.execute_script('document.getElementById("password").value="SuperSecretPassword!";')
    driver.find_element('xpath','//button').click()
    WebDriverWait(driver, 2).until(EC.presence_of_element_located((by.ID, 'flash')))
    assert 'username' in driver.find_element(by.ID, "flash").text

    driver.quit()
    
