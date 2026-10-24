import pytest
from driver_manager import driver_manager


def pytest_addoption(parser):
    parser.addoption(
        "-H", "--headed",
        action="store_true",
        default=False,
        help="Run browser in headed mode",
    )


@pytest.fixture
def driver(request):
    yield driver_manager.start(headed=request.config.getoption("--headed"))
    driver_manager.quit()
