from selenium.webdriver.common.by import By as by
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.wait import WebDriverWait

from driver_factory import driver_factory



def test_title():

    driver = driver_factory.get_driver()
    driver.get("https://the-internet.herokuapp.com/")

    assert "The Internet" in driver.title

    driver.quit()


def test_ab_testing():

    driver = driver_factory.get_driver()
    driver.get("https://the-internet.herokuapp.com/")

    link = driver.find_element('xpath', '//a[text()="A/B Testing"]')
    link.click()

    # get the first line of text on the page
    page_text = driver.find_element(by.TAG_NAME, 'body').text
    first_line = next(line for line in page_text.splitlines() if line.strip())
    
    assert first_line == 'A/B Test Variation 1' or first_line == 'A/B Test Control'

    driver.quit()


def test_ab_testing_elemental_selenium_link():

    driver = driver_factory.get_driver()
    driver.get("https://the-internet.herokuapp.com/")

    link = driver.find_element('xpath', '//a[text()="A/B Testing"]')
    link.click()

    link = driver.find_element('xpath','//a[text()="Elemental Selenium"]')
    link.click()

    driver.switch_to.window(driver.window_handles[1])

    assert "Elemental Selenium" in driver.title

    driver.quit()


def test_add_elements():

    driver = driver_factory.get_driver()
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

    driver = driver_factory.get_driver()
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

    driver = driver_factory.get_driver()
    driver.get("https://admin:admin@the-internet.herokuapp.com/basic_auth")

    # get the first line of text on the page
    page_text = driver.find_element(by.TAG_NAME, 'body').text
    first_line = next(line for line in page_text.splitlines() if line.strip())

    assert first_line == 'Basic Auth'

    driver.quit()


def test_challenging_dom_three_buttons():

    driver = driver_factory.get_driver()
    driver.get("https://the-internet.herokuapp.com/")
    driver.find_element('xpath', '//a[text()="Challenging DOM"]').click()
    
    button_text1_b = driver.find_element('xpath', '//a[contains(@class, "button")]').text
    button_text2_b = driver.find_element('xpath', '//a[contains(@class, "button alert")]').text
    button_text3_b = driver.find_element('xpath', '//a[contains(@class, "button success")]').text

    driver.find_element('xpath', '//a[contains(@class, "button")]').click()

    button_text1_a = driver.find_element('xpath', '//a[contains(@class, "button")]').text
    button_text2_a = driver.find_element('xpath', '//a[contains(@class, "button alert")]').text
    button_text3_a = driver.find_element('xpath', '//a[contains(@class, "button success")]').text

    #This test is to verify that the text on the three buttons changes after the button is clicked

    text_before_click = [button_text1_b, button_text2_b, button_text3_b]
    text_after_click = [button_text1_a, button_text2_a, button_text3_a]

    assert text_before_click != text_after_click, "the buttons texts before clicking the top button matches the text after clicking it"

    driver.quit()


def test_challenging_dom_edit_delete_links():

    driver = driver_factory.get_driver()
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


def test_broken_images():

    driver = driver_factory.get_driver()
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

    driver = driver_factory.get_driver()
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

    driver = driver_factory.get_driver()
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
  
    driver = driver_factory.get_driver()
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

    driver = driver_factory.get_driver()    
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

    driver = driver_factory.get_driver()     
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

    driver = driver_factory.get_driver()     
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


def test_hovers():
    
    driver = driver_factory.get_driver()     
    driver.get("https://the-internet.herokuapp.com/")
    
    actions = ActionChains(driver)

    driver.find_element('xpath', '//a[text()="Hovers"]').click()
    
    figures = driver.find_elements(by.CLASS_NAME, 'figure')

    for i,fig in enumerate(figures):
        i += 1
        actions.move_to_element(fig).perform()
        EC.element_to_be_clickable((by.LINK_TEXT, "View profile"))(driver).click()
        assert EC.url_contains(f"users/{i}")(driver)
        driver.back()

    driver.quit()

    
def test_form_auth():
    driver = driver_factory.get_driver()  
    driver.get("https://the-internet.herokuapp.com/")
    
    driver.find_element('xpath', '//a[text()="Form Authentication"]').click()
    actions = ActionChains(driver)

    actions.send_keys_to_element(driver.find_element(by.ID, 'username'), 'tomsmith').perform()
    actions.send_keys_to_element(driver.find_element(by.ID, 'password'), 'SuperSecretPassword!').perform()

    driver.find_element('xpath','//button[@type ="submit"]').click()

    WebDriverWait(driver, 1).until(EC.url_contains('secure'))
    assert driver.current_url == "https://the-internet.herokuapp.com/secure"
    
    driver.quit()


def test_form_auth_errors():

    driver = driver_factory.get_driver()     
    driver.get("https://the-internet.herokuapp.com/")
    
    driver.find_element('xpath', '//a[text()="Form Authentication"]').click()
    actions = ActionChains(driver)
    # Both Blank
    driver.find_element('xpath','//button[@type ="submit"]').click()
    WebDriverWait(driver, 1).until(EC.presence_of_element_located((by.ID, 'flash')))
    assert 'username' in driver.find_element(by.ID, "flash").text

    # Correct username, Blank password
    actions.send_keys_to_element(driver.find_element(by.ID, 'username'), 'tomsmith').perform()
    driver.find_element('xpath','//button[@type ="submit"]').click()
    WebDriverWait(driver, 1).until(EC.presence_of_element_located((by.ID, 'flash')))
    assert 'password' in driver.find_element(by.ID, "flash").text

    # Blank username, Correct password
    actions.send_keys_to_element(driver.find_element(by.ID, 'password'), 'SuperSecretPassword!').perform()
    driver.find_element('xpath','//button[@type ="submit"]').click()
    WebDriverWait(driver, 1).until(EC.presence_of_element_located((by.ID, 'flash')))
    assert 'username' in driver.find_element(by.ID, "flash").text
    
    driver.quit()
    
    
    
    