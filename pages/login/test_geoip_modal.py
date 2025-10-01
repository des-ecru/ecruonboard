import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

def test_verify_location_modal( driver) -> None:
    # self.setup_driver()
    # driver = self.driver

    print("Location Modal Test")
    time.sleep(5)
    geoip_modal = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '[id^="headlessui-dialog-panel"]'))
    )
    if geoip_modal.is_displayed():
        print("GeoIP modal is visible")
        close_button = geoip_modal.find_element(By.CSS_SELECTOR, '#headlessui-dialog-title-\:r1\: > svg')
        
        close_button.click()
        time.sleep(2)
        print("GeoIP modal is now hidden. Continuing with the test")
    else:
        print("GeoIP modal is hidden. Continuing with test.")