import pytest
from driver_factory import driver_factory


def pytest_addoption(parser):
    parser.addoption(
        "-H", "--headed",
        action="store_true",
        default=False,
        help="Run browser in headed mode",
    )


@pytest.fixture
def driver(request):
    driver = driver_factory.get_driver(headless=not request.config.getoption("--headed"))
    yield driver
    driver.quit()
