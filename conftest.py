import pytest
from driver_factory import DriverFactory


def pytest_addoption(parser):
    parser.addoption(
        "-H", "--headed",
        action="store_true",
        default=False,
        help="Run browser in headed mode",
    )


@pytest.fixture
def driver(request):
    driver = DriverFactory.get_driver(headed=request.config.getoption("--headed"))
    yield driver
    driver.quit()
