import pytest
from driver_manager import set_headless


def pytest_addoption(parser):
    parser.addoption(
        "-H",
        action="store_true",
        default=False,
        help="Run browser in headed mode",
    )


def pytest_configure(config):
    headed = config.getoption("-H")
    set_headless(not headed)
