"""Element classes that page objects use to declare their elements.

Each element is created with a locator, e.g. Checkbox(('xpath', '//input')),
and finds itself in the current browser (driver_manager.driver) each time it's used.
An element whose locator matches several elements also stands for the whole group.
"""

from selenium.webdriver.support.ui import Select, WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC

from driver_manager import driver_manager


class BaseElement:
    """Shared behavior for all elements: finding them and delegating to Selenium.

    Any attribute an element class doesn't define is passed through to the
    underlying Selenium WebElement, so click(), is_selected(), text, and the
    rest of WebElement work directly on elements.

    A locator may match several elements. Without an index, the element is
    the first match in page order; the others are ignored, with no error or
    warning. Use count(), nth(), and all() to work with every match.

    In page objects, an element's name ends with its type. A singular name
    (foo_button) means the locator matches exactly one element. A plural name
    (foo_buttons) means it may match one or more; use such an element only
    through count(), nth(), and all(), e.g. foo_buttons.nth(0).click() rather
    than foo_buttons.click().
    """

    def __init__(self, locator, index=None):
        """Store the locator and which match to use.

        The locator is a (strategy, value) pair such as ('xpath', '//h3'). The
        index picks the Nth match (counting from 0). With no index, the element
        is the first match, even if the locator matches more than one.
        """
        self.locator = locator
        self.index = index

    def __getattr__(self, name):
        """Pass any attribute this class doesn't define to the Selenium WebElement."""
        # never delegate dunder names: Python and tools (copy, pickle, debuggers) probe for them,
        # and delegating would hit the browser or recurse forever on half-built objects
        if name.startswith("__") and name.endswith("__"):
            raise AttributeError(name)
        return getattr(self.element(), name)

    def element(self):
        """Wait for the element to exist, then return it as a Selenium WebElement.

        Without an index this is the first match of the locator; with one, it's
        the match at that index.
        """
        if self.index is None:
            return wait(driver_manager.driver, 10).until(
                EC.presence_of_element_located(self.locator))
        else:
            return wait(driver_manager.driver, 10).until(lambda driver: self._nth_match(driver))

    def _nth_match(self, driver):
        """Return the match at self.index, or False if there aren't that many yet."""
        matches = driver.find_elements(*self.locator)
        if len(matches) > self.index:
            return matches[self.index]
        else:
            return False

    def count(self):
        """Return how many elements the locator currently matches, without waiting."""
        return len(driver_manager.driver.find_elements(*self.locator))

    def nth(self, index):
        """Return an element of the same type for the match at index (counting from 0)."""
        # the new element is found when it's used, so it's "the Nth match at that moment"
        return type(self)(self.locator, index)

    def all(self):
        """Return one element per current match, in page order."""
        return [self.nth(i) for i in range(self.count())]


class Button(BaseElement):
    """A button. Actions like click() come from the Selenium element."""


class Checkbox(BaseElement):
    """A checkbox."""

    def toggle(self):
        """Click the checkbox, flipping it between checked and unchecked."""
        wait(driver_manager.driver, 10).until(EC.element_to_be_clickable(self.locator))
        self.element().click()

    def check(self):
        """Check the checkbox if it isn't already checked."""
        if not self.element().is_selected():
            self.toggle()

    def uncheck(self):
        """Uncheck the checkbox if it's currently checked."""
        if self.element().is_selected():
            self.toggle()


class Dropdown(BaseElement):
    """A dropdown (a <select> element)."""

    def __getattr__(self, name):
        """Pass undefined attributes to Selenium's Select helper, or else to the WebElement."""
        # never delegate dunder names (see BaseElement.__getattr__)
        if name.startswith("__") and name.endswith("__"):
            raise AttributeError(name)
        el = self.element()
        select = Select(el)
        if hasattr(select, name):
            return getattr(select, name)
        return getattr(el, name)

    def option(self, text):
        """Return the option with the given visible text, waiting for it to appear."""
        locator = ('xpath', f'./option[normalize-space()="{text}"]')
        # search within this dropdown's <select>, so an option in another dropdown can't match
        return wait(driver_manager.driver, 10).until(
            lambda driver: self.element().find_element(*locator))

    def select(self, choice):
        """Select an option by its visible text (a str) or its index (an int)."""
        if isinstance(choice, int):
            self.select_by_index(choice)
        elif isinstance(choice, str):
            self.select_by_visible_text(choice)
        else:
            raise TypeError(f"select() takes option text (str) or an index (int), not {type(choice).__name__}")


class Image(BaseElement):
    """An image."""

    def is_broken(self):
        """Return True if the image failed to load."""
        # an image that loaded has a natural (intrinsic) width; a broken one has 0
        return self.element().get_property("naturalWidth") == 0


class Link(BaseElement):
    """A link. Actions like click() come from the Selenium element."""


class Text(BaseElement):
    """Text that tests read, such as a heading or label (e.g. .text)."""
