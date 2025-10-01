import pytest
from utilities.drivers.driver_manager import Driver_Manager


@pytest.fixture(scope="function")
def driver():
    # Setup: initialize the WebDriver
    driver_instance = Driver_Manager().get_driver()
    yield driver_instance
    # Teardown: quit the driver after test
    driver_instance.quit()