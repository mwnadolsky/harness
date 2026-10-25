"""Page object for the Broken Images page (/broken_images)."""

from pages.the_internet.base import BasePage


class BrokenImagesPage(BasePage):
    """The Broken Images page: two broken images and one working one."""

    header = '//h3'
    images = '//div[@class="example"]/img'
    image1 = '//img[@src="asdf.jpg"]'
    image2 = '//img[@src="hjkl.jpg"]'
    image3 = '//img[@src="img/avatar-blank.jpg"]'
