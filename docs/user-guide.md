# Harness User Guide

> **Draft.** First pass at describing how the harness works and the conventions for writing tests in it. Expect heavy edits.

This harness runs Selenium tests with pytest against [the-internet](https://the-internet.herokuapp.com/), a practice site full of awkward web pages. It has two kinds of tests:

- **`test_po.py`:** page-object tests. Tests talk to *page objects* and *elements*, never to Selenium elements directly. This is the style new tests should use.
- **`test_raw.py`:** the same kinds of checks written with plain Selenium. It's the original suite, and tests are gradually being ported from it to `test_po.py`.

## Contents

1. [Running tests](#running-tests)
2. [Project layout](#project-layout)
3. [Writing a page-object test](#writing-a-page-object-test)
4. [Page objects](#page-objects)
5. [Elements](#elements)
6. [Groups of elements](#groups-of-elements)
7. [Naming conventions](#naming-conventions)
8. [Why elements: no more waiting by hand](#why-elements-no-more-waiting-by-hand)
9. [What raw Selenium is allowed in page-object tests](#what-raw-selenium-is-allowed-in-page-object-tests)
10. [Raw tests and the implicit wait](#raw-tests-and-the-implicit-wait)
11. [Code style](#code-style)
12. [Decision records](#decision-records)

## Running tests

Set up once:

```sh
python -m venv .venv
.venv/bin/pip install -r requirements.txt
```

Run tests by **marker**:

| Command | Runs |
|---|---|
| `pytest -m smoke` | a few fast tests |
| `pytest -m regression_po` | every test in `test_po.py` |
| `pytest -m regression_raw` | every test in `test_raw.py` |
| `pytest` | everything |

Markers are registered in `pytest.ini`, and pytest runs with `--strict-markers`, so a misspelled or unregistered marker is an error, not a silent no-op. To add a marker, register it in `pytest.ini` first.

**Headless by default.** Tests run in a headless Chrome. Add **`-H`** (or `--headed`) to watch the browser:

```sh
pytest -m smoke -H
```

Either way, the window is maximized, and headless runs get a 1920×1080 screen. See [decision record 0001](decisions/0001-maximize-window.md) for why it's maximized and not fullscreen.

Add `-v` to see each test's name and result.

## Project layout

```
conftest.py          the driver fixture and the -H/--headed option
driver_manager.py    starts and quits Chrome; holds the current driver
elements.py          element classes (Button, Checkbox, Dropdown, ...)
pages/
  the_internet/      one page object per page of the-internet
    base.py          BasePage: elements shared by every page
    home.py          HomePage
    checkboxes.py    CheckboxesPage
    ...
test_po.py           page-object tests
test_raw.py          plain-Selenium tests
pytest.ini           markers and pytest options
docs/decisions/      decision records
```

**The `driver` fixture** starts a fresh Chrome for every test, opens the-internet's home page, hands the browser to the test, and quits it afterward. Every test that takes `driver` starts on the home page in a clean browser, with no cookies or state left over from earlier tests.

## Writing a page-object test

```python
def test_checkboxes(driver):

    page = HomePage()

    page.checkboxes_link.click()

    page = CheckboxesPage()

    assert page.header_text.text == "Checkboxes"
    assert not page.checkbox_1_checkbox.is_selected()

    page.checkbox_1_checkbox.toggle()

    assert page.checkbox_1_checkbox.is_selected()
```

**`page` is always the page currently on screen.** Tests start on the home page, so they start with `page = HomePage()`. Whenever an action takes the browser to a different page, reassign `page` right after it. Reading the test top to bottom then tells you which page you're on at every line.

**Take `driver` as a parameter** even if the test never uses it directly. Requesting the fixture is what starts the browser.

**Layout:** group the lines into blocks separated by blank lines: actions, then the assertions about them. Don't narrate with comments. A comment is for something a reader wouldn't otherwise understand, like why a test repeats something 20 times.

**No docstrings on tests.** What a test checks belongs in the manual test documentation, not in the code.

## Page objects

A page object is a class that **declares the elements on one page**, and nothing else:

```python
class DropdownPage(BasePage):
    """Page object for the Dropdown page."""

    header_text = Text(('xpath', '//h3'))
    option_dropdown = Dropdown(('xpath', '//select[@id="dropdown"]'))
```

- **Locators only.** Page objects hold no methods like `select_option()` or `go_to_checkboxes()`. Per-page helper functions pile up and become hard to maintain. Behavior lives in the [element classes](#elements), where it's written once and shared by every page.
- **Elements are class attributes; tests use instances.** Declare elements at class level, as above, and create an instance in tests: `page = DropdownPage()`. Every instance shares the same element objects, so creating one is effectively free.
- **The locator is written inline,** as a `(strategy, value)` pair, usually XPath.
- **Every page object subclasses `BasePage`,** which declares the elements every page shares (the flash message, the "Fork me on GitHub" link, the footer link).
- **One page object per page,** in `pages/<site>/`. Each site gets its own package, so `pages/the_internet/` holds the-internet's pages.

## Elements

Element classes live in `elements.py`:

| Class | For | Extras beyond Selenium |
|---|---|---|
| `Button` | buttons | none |
| `Checkbox` | checkboxes | `toggle()`, `check()`, `uncheck()` |
| `Dropdown` | `<select>` dropdowns | `option(text)`, `select(text_or_index)`, plus everything on Selenium's `Select` |
| `Image` | images | `is_broken()` |
| `Link` | links | none |
| `Text` | text you read, like headings | none |

**An element is a recipe, not a found element.** It stores a locator and **finds itself again every time you use it.** That means it can't go stale, and it doesn't matter whether the page has reloaded since the page object was defined.

**Every lookup waits.** Before using an element, the harness waits up to 10 seconds for it to exist on the page. See [Why elements](#why-elements-no-more-waiting-by-hand).

**Everything else comes from Selenium.** Anything an element class doesn't define is passed straight through to the underlying Selenium `WebElement`. So `page.submit_button.click()`, `page.header_text.text`, `page.checkbox_1_checkbox.is_selected()` and the rest of the `WebElement` API all work directly on elements. `Dropdown` passes attributes to Selenium's `Select` helper first, so `select_by_value()`, `options` and the like work too.

To add behavior that Selenium doesn't have, add a method to the right element class (or to `BaseElement`, if every element should have it). Don't add it to a page object.

## Groups of elements

One element can stand for **every** match of its locator. Some pages have a varying number of the same thing, like the Delete buttons on Add/Remove Elements. Declare the group once:

```python
delete_buttons = Button(('xpath', '//div[@id="elements"]/button[text()="Delete"]'))
```

and use it through the group methods, available on every element:

| Method | Returns |
|---|---|
| `count()` | how many elements match right now. Doesn't wait, since 0 is a valid answer. |
| `nth(i)` | an element of the same type for the i-th match, counting from 0 |
| `all()` | one element per current match, in page order |
| `random()` | an element for a randomly chosen match. Waits for at least one match first. |

```python
assert page.delete_buttons.count() == 5

page.delete_buttons.nth(0).click()
page.delete_buttons.random().click()
```

**How it works:** `nth(2)` doesn't search the page. It returns a new element that remembers "the third match of this locator", and that element is looked up when you use it. So it means **the third match at that moment**. If an earlier match disappears, positions shift: after you delete the first button, `nth(2)` refers to the button that used to be fourth.

Some behaviors to know:
- **An index past the end waits, then fails.** `nth(5)` with only 2 matches waits 10 seconds for a sixth match to appear, then raises a `TimeoutException`. A single element that never appears fails the same way.
- **A negative index on an empty group fails immediately** with an `IndexError`.
- **An element used without an index is the first match.** If a locator matches several elements and you use the element directly (`page.foo_buttons.click()`), you get the first match in page order. There's no error or warning about the others. That's why the naming rule below matters.

## Naming conventions

**An element's name ends with its type:** `checkboxes_link`, `header_text`, `submit_button`, `option_dropdown`. The suffix tells you what you can do with it without opening the page object. It still applies when it reads oddly: the home page's link to Redirect Link is `redirect_link_link`.

**Singular means exactly one; plural means a group:**

| Name | Means | Use it |
|---|---|---|
| `foo_button` | the locator matches exactly one element | directly: `page.foo_button.click()` |
| `foo_buttons` | the locator may match one or more | only through `count()`, `nth()`, `all()` and `random()` |

So write `page.delete_buttons.nth(0).click()`, never `page.delete_buttons.click()`. The longer form says which button you mean. The short one would silently click the first, which reads like "click all the buttons". The plural rule is mechanical, even when the plural reads oddly: a group of `Text` elements is `foo_texts`.

**Page objects are named after the URL path:** the page at `/bar/baz` lives in `bar_baz.py` as `BarBazPage`. For example, `/abtest` is `abtest.py` and `AbtestPage`, and `/add_remove_elements/` is `add_remove_elements.py` and `AddRemoveElementsPage`.

**`LoginPage` is reserved** for a future login fixture. (Open question: what to call the page object for a site's own `/login` page.)

## Why elements: no more waiting by hand

The biggest practical benefit of elements is that **they prevent slow-page-load failures, and they remove most of the finicky explicit waiting** that plain Selenium tests need.

In plain Selenium, `driver.find_element(...)` looks once. If the page is still loading, it fails right away. The usual fix is an explicit wait at that spot:

```python
WebDriverWait(driver, 10).until(EC.presence_of_element_located(('xpath', '//a[text()="Add/Remove Elements"]'))).click()
```

and then the same fix at the next spot, and the next. Each test has to get every wait right on its own. When one is missed, you debug it test by test, even though it's really one systemic problem.

Elements build that wait into every lookup, so tests just say `page.add_remove_elements_link.click()`. The fix lives in one place, and it covers every test.

**This has already happened in this project.** `test_raw.py` had three slow-load failures (`test_slider`, `test_form_auth_errors` and `test_broken_images`), each a raw `find_element` running before the page was ready. Fixing them needed an implicit wait for the whole file, with an opt-out for tests that it slowed down (see [below](#raw-tests-and-the-implicit-wait)). `test_po.py` hasn't had a slow-load failure.

**General principle:** put anything with a systemic failure mode behind an abstraction, so it's fixed in one place for every test.

## What raw Selenium is allowed in page-object tests

The goal is **no raw Selenium for element work** in `test_po.py`: no `driver.find_element`, no raw `WebElement`s, no hand-written waits for elements. Use page objects and elements.

**Driver actions are fine as raw Selenium:** `driver.refresh()`, `driver.get(...)`, `driver.back()`, `driver.delete_all_cookies()`, `driver.title`, `driver.current_url` and the like. They act on the browser as a whole and have nothing to wait for. Wrapping them would just add a pass-through layer that never fixes anything. The A/B tests use them like this:

```python
for _ in range(20):
    driver.delete_all_cookies()
    driver.refresh()
    seen.add(page.header_text.text)
```

**The exception: driver actions that wait on the browser.** These include switching to a newly opened window, handling an alert, and switching into a frame. They have the same kind of race as element lookups: the window, alert or frame may not exist yet. When one of these causes a failure, the plan is a driver abstraction that adds the needed waits to those actions and passes everything else straight through to Selenium, the same way elements do.

## Raw tests and the implicit wait

`test_raw.py` has an autouse fixture that gives every test in that file a **10-second implicit wait**: every `find_element` waits up to 10 seconds for its element. It applies only to `test_raw.py`. Page-object tests use their elements' explicit waits, and mixing the two kinds of wait makes wait times unpredictable.

**The catch:** with an implicit wait, `find_elements` only returns an empty list after waiting the full 10 seconds. So checking that something is *absent* gets slow. Tests that do that can opt out with the `no_implicit_wait` marker and use explicit waits instead:

```python
@pytest.mark.no_implicit_wait
def test_add_elements(driver):
    ...
```

## Code style

- **Docstrings (PEP 257) on harness code:** every module, public class and public method. Describe what the thing does in general terms. Don't list a page's elements or name individual elements. **Tests don't get docstrings.**
- **Comments only for what isn't obvious,** such as why something waits or why a number was chosen. Not as descriptions; that's what docstrings are for.
- **In classes, dunder methods come first, with `__init__` first,** then regular methods.
- **Prefer explicit `if`/`else`** even where an early `return` would do.
- **Element-related wait timeouts are 10 seconds** unless there's a reason otherwise.

## Decision records

Significant decisions, especially ones that took investigation, are recorded in `docs/decisions/NNNN-short-title.md`. Each one has a **Context** (the problem and what was found) and a **Decision** section with one bullet per decision and a one-sentence reason. When you change something a record covers, read the record first. Then update it, or write a new one that replaces it.

| Record | Decision |
|---|---|
| [0001](decisions/0001-maximize-window.md) | Maximize the browser window instead of using fullscreen |
