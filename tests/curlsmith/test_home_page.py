import time
# import pytest

# from utilities.drivers.driver_manager import Driver_Manager
# from selenium.webdriver.remote.webdriver import WebDriver

# from utilities.base.verifications import Verifications
# from utilities.base.verifications import UI_Actions

from pages.curlsmith.curlsmith_locators import CurlSmithLocators
from selenium.webdriver.remote.webelement import WebElement


url = "https://curlsmith.com/"


class Test_Home_Page:
    def test_home_page_loads(self, driver):
        driver.get(url)
        time.sleep(2)

        self.test_verify_sign_up_modal(driver)
        # self.test_verify_home_page(driver)
        driver.quit()
    
    def test_verify_sign_up_modal(self, driver):
        print("Verify the Sign Up Modal ")
        geoip_modal: WebElement = driver.get_element(By.CSS_SELECTOR, CurlSmithLocators.sign_up_modal)
        # WebDriverWait(driver, 10).until(
        #     EC.presence_of_element_located((By.CSS_SELECTOR, '[id^="headl   essui-dialog-panel"]'))
        # )
        if geoip_modal.is_displayed():
            print("GeoIP modal is visible")
            close_button = geoip_modal.find_element(By.CSS_SELECTOR, 'svg.cursor-pointer')
            close_button.click()
            time.sleep(2)
            print("GeoIP modal is now closed. Continuing with the test")

