from selenium import webdriver
from selenium.webdriver.common.by import By as by


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
    driver.get("https://admin:admin@the-internet.herokuapp.com")
    driver.find_element('xpath', '//a[text()="Broken Images"]').click()

    #this finds all images on this page and creates the list called images
    images = driver.find_elements(by.TAG_NAME, 'img')

    broken_count = 0
    question_list = []
    for img in images:
        # With Javascript I can see if the natural width is 0 and is therefore broken
        natural_width = driver.execute_script("return arguments[0].naturalWidth", img)
        image_src = img.get_attribute('src') or img.get_attribute('data-src') or 'No source'

        if natural_width == 0:
            broken_count += 1
            question_list.append(image_src)
        else:
            question_list.append(image_src)
    
    assert 2 == broken_count, f"broken images was two out of four, which of these are broken? {question_list}"

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

def test_dynamic_content():

    driver=webdriver.Chrome()
    driver.get("https://the-internet.herokuapp.com/")
    driver.find_element('xpath','//a[text()="Dynamic Content"]').click()

    # Keeping lists of srcs of images and text properties of elements for readable comparison
    images = []
    texts = []
    
    # Example images and texts have separate classes on this page, find each and add to appropriate list
    for i in driver.find_elements('xpath','//div[@class="large-2 columns"]//img'):
        images.append(i.get_attribute('src'))

    for t in driver.find_elements('xpath','//div[@class="large-10 columns"]'):
        texts.append(t.text)

    driver.get("https://the-internet.herokuapp.com/")
    driver.find_element('xpath','//a[text()="Dynamic Content"]').click()

    # Separate list for new elements, to compare with original
    new_images= []
    new_texts = []

    for i in driver.find_elements('xpath','//div[@class="large-2 columns"]//img'):
        new_images.append(i.get_attribute('src'))

    for t in driver.find_elements('xpath','//div[@class="large-10 columns"]'):
        new_texts.append(t.text)

    assert new_images != images
    assert new_texts != texts
    #print("Change Happened")

    driver.quit()


def test_dynamic_content_with_static():

    driver=webdriver.Chrome()
    driver.get("https://the-internet.herokuapp.com/")
    driver.find_element('xpath','//a[text()="Dynamic Content"]').click()
    driver.find_element('xpath','//a[text()="click here"]').click()

    images = []
    texts = []
    
    for i in driver.find_elements('xpath','//div[@class="large-2 columns"]//img'):
        images.append(i.get_attribute('src'))

    for t in driver.find_elements('xpath','//div[@class="large-10 columns"]'):
        texts.append(t.text)

    # Clicking here to keep some content static
    driver.find_element('xpath','//a[text()="click here"]').click()

    new_images= []
    new_texts = []

    # Only appends to new list if it is a brand new src or new text.
    for i in driver.find_elements('xpath','//div[@class="large-2 columns"]//img'):
        if i.get_attribute('src') not in images:
            new_images.append(i.get_attribute('src'))

    for t in driver.find_elements('xpath','//div[@class="large-10 columns"]'):
        if t.text not in texts:
            new_texts.append(t.text)

    #print(f"New Images:{new_images} \nNew Text:{new_texts}")
    assert len(new_images) != 0 or len(new_texts) != 0

    driver.quit()


