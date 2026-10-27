"""Pytest configuration: options and fixtures."""

import pytest
from driver_manager import driver_manager


def pytest_addoption(parser):
    """Add the -H/--headed option for running the browser visibly."""
    parser.addoption(
        "-H", "--headed",
        action="store_true",
        default=False,
        help="Run browser in headed mode",
    )


@pytest.fixture
def driver(request):
    """Start a browser on the-internet's home page, yield it, and quit it afterward.

    The browser is headless unless pytest is run with -H/--headed. While the
    test runs, the same browser is also available as driver_manager.driver.
    """
    driver = driver_manager.start(headed=request.config.getoption("--headed"))
    driver.get("https://the-internet.herokuapp.com/")
    yield driver
    driver_manager.quit()
