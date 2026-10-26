"""Page object for the Broken Images page (/broken_images)."""

from pages.the_internet.base import BasePage
from elements import Image, Text


class BrokenImagesPage(BasePage):
    """Page object for the Broken Images page."""

    header_text = Text(('xpath', '//h3'))
    images = '//div[@class="example"]/img'
    image_1_image = Image(('xpath', '//img[@src="asdf.jpg"]'))
    image_2_image = Image(('xpath', '//img[@src="hjkl.jpg"]'))
    image_3_image = Image(('xpath', '//img[@src="img/avatar-blank.jpg"]'))
