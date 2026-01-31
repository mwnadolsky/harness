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
    #NOTES: I tried multiple times to see if an alert is present when the pop up is present.
    #       I kept getting the time out error for these alerts so the pop up is assumed to not
    #       be an alert.
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

    #NOTES:  The same handles kept popping up on my output, there are not two handles only one, so this pop up isn't a handle 
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

    #NOTES:  So here is where I ended my search. I am assuming this is a "Shadow DOM". You can search that.
    # With my DevTools I'm trying to record the DOM tree while I'm interacting with this pop-up to see if I can 
    # view any of it's html code, but I can't. 
    # I can't find a way to interact with this pop-up's elements.
    # The developer of pop-ups especially sign in pop ups would like to make the html difficult to see for automators
    # If this is a shadow host type of a pop up then maybe this will find it. But I don't know if I'm using the right shadow host 
    # I guessed at the-internet.herokuapp.com and the-internet.herokuapp.com/basic_auth for the shadow host names. I don't know how to find the shadow host name

    #shadow_host = driver.find_element(By.CSS_SELECTOR, "css-selector-of-shadow-host")              #I got this from Generic Google search


    # Find all elements with shadow roots
    shadow_hosts = driver.execute_script("""
    return Array.from(document.querySelectorAll('*'))
        """)

    print('All shadow hosts:', shadow_hosts)
    print('Number of shadow hosts found:', len(shadow_hosts))


    shadow_host = driver.find_element(by.CSS_SELECTOR, "the-internet.herokuapp.com/basic_auth")     # I replaced it with this, I was just guessing here. I didn't look into how to find the above selector.

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



#NOTES:  To see shadow hosts (specifically the hidden user-agent shadow DOM) in Chrome DevTools, you need to enable a specific setting within the DevTools preferences. 
# Steps to enable "Show user agent shadow DOM"
# Open Chrome DevTools. You can do this by right-clicking on any element on the web page and selecting Inspect, or by pressing F12, or Ctrl+Shift+I (Windows/Linux) / Command+Option+I (Mac).
# Open the DevTools Settings. Click the Settings cog icon (⚙️) in the top-right corner of the DevTools panel, or press F1.
# Navigate to the "Preferences" tab (which is the default view).
# Find the "Elements" section and check the box for "Show user agent shadow DOM".
# Close the Settings panel. 

#Here are some additional notes for where I left off.
#Google search this: "shadow dom elements in selenium", "in chrome devtools record DOM tree", "Tell me about shadow hosts for pop ups", "DevTools can't interact with DOM while popup is open".  
#The above is where I left off. I have been staring at this issue for too long and I have to take a break.

#The below code didn't get anything useful
    # Find all elements with shadow roots
    shadow_hosts = driver.execute_script("""
    return Array.from(document.querySelectorAll('*'))
        .filter(el => el.shadowRoot)
        .map(el => el);
    """)
    #Above output is nothing

    shadow_hosts1 = driver.execute_script("""
    return Array.from(document.querySelectorAll('*'))""")
