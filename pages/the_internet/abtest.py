"""Page object for the A/B Testing page (/abtest)."""

from pages.the_internet.base import BasePage
from elements import Text


class AbtestPage(BasePage):
    """Page object for the A/B Testing page."""

    # the server sends "No A/B Test"; the page's Optimizely script replaces it with the visitor's variant
    header_text = Text(('xpath', '//h3'))
