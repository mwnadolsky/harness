"""Element classes that page objects use to declare their elements.

Each element is created with a locator, e.g. Checkbox(('xpath', '//input')),
and finds itself in the current browser (driver_manager.driver) each time it's used.
"""

from selenium.webdriver.support.ui import Select, WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC

from driver_manager import driver_manager


class BaseElement:
    """Shared behavior for all elements: finding them and delegating to Selenium.

    Any attribute an element class doesn't define is passed through to the
    underlying Selenium WebElement, so click(), is_selected(), text, and the
    rest of WebElement work directly on elements.
    """

    def __init__(self, locator):
        """Store the locator, a (strategy, value) pair such as ('xpath', '//h3')."""
        self.locator = locator

    def element(self):
        """Wait for the element to exist, then return it as a Selenium WebElement."""
        return wait(driver_manager.driver, 10).until(
            EC.presence_of_element_located(self.locator))

    def __getattr__(self, name):
        """Pass any attribute this class doesn't define to the Selenium WebElement."""
        # never delegate dunder names: Python and tools (copy, pickle, debuggers) probe for them,
        # and delegating would hit the browser or recurse forever on half-built objects
        if name.startswith("__") and name.endswith("__"):
            raise AttributeError(name)
        return getattr(self.element(), name)


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

    def option(self, text):
        """Return the dropdown's option with the given visible text."""
        return Option(self, text)

    def select(self, text):
        """Select the option with the given visible text."""
        Select(self.element()).select_by_visible_text(text)


class Link(BaseElement):
    """A link. Actions like click() come from the Selenium element."""


class Option(BaseElement):
    """An option in a Dropdown, found by its visible text."""

    def __init__(self, dropdown, text):
        """Store the Dropdown this option belongs to and the option's visible text."""
        super().__init__(('xpath', f'./option[normalize-space()="{text}"]'))
        self.dropdown = dropdown

    def element(self):
        """Wait for the option to exist inside its dropdown, then return it."""
        # search within the dropdown's <select>, so an option in another dropdown can't match
        return wait(driver_manager.driver, 10).until(
            lambda driver: self.dropdown.element().find_element(*self.locator))


class Text(BaseElement):
    """Text that tests read, such as a heading or label (e.g. .text)."""
