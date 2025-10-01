import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

class Test_Login_Page:   
    def test_nav_to_page(self, env) -> None:
        driver = self.setup_driver()
        url = "https://www.varley.com/account/login"
        driver.get(url)
        time.sleep(2)
        
        self.verify_location_modal(driver)
        self.test_empty_login(driver)
        self.test_unsuccessful_login(driver)
        self.test_successful_login(driver)
        driver.quit()

    def setup_driver(self):
        chrome_options = Options()
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-popup-blocking")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--start-maximized")
        chrome_service = ChromeService(
            ChromeDriverManager().install()
        )
        driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
        return driver
    
    def verify_location_modal(self, driver) -> None:
        print("Location Modal Test")
        time.sleep(5)
        geoip_modal = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '[id^="headlessui-dialog-panel"]'))
        )
        if geoip_modal.is_displayed():
            print("GeoIP modal is visible")
            close_button = geoip_modal.find_element(By.CSS_SELECTOR, 'svg.cursor-pointer')
            close_button.click()
            time.sleep(2)
            print("GeoIP modal is now closed. Continuing with the test")
        else:
            print("GeoIP modal is closed. Continuing with test.")
    
    def test_empty_login(self, driver) -> None:
        print("\nVerify Empty Login")
        login_section = driver.find_element(By.CSS_SELECTOR, 'main[class="relative grow"] div[class="mx-auto"]')  
        assert login_section.is_displayed(), "The login section is not displayed"
        print("Login section is displayed")
        
        sign_in_button = driver.find_element(By.CSS_SELECTOR, 'form[action="/account/login"] button[type="submit"]')
        print("Clicking the Sign in button immediately..")
        sign_in_button.click()
        time.sleep(10)
        
        error_notification = driver.find_element(By.CSS_SELECTOR, '[class^="mb-6"] p')
        assert error_notification.is_displayed(), "No Error Notification displayed"
        expected_message = "Please provide both an email and a password."
        assert expected_message == error_notification.text, "Expected Message is not correct"
        print("Error Message expected")
        
    def test_unsuccessful_login(self, driver) -> None:
        driver.refresh()
        print("\nVerify Unsuccessful Login")
        login_section = driver.find_element(By.CSS_SELECTOR, 'main[class="relative grow"] div[class="mx-auto"]')  
        assert login_section.is_displayed(), "The login section is not displayed"
        print("Login section is displayed")

        # Input valid email
        print("Entering invalid email")
        email_input = driver.find_element(By.CSS_SELECTOR, 'input[name="email"]')
        email_input.send_keys("lourds@ecrubox.com")

        # Input valid password
        print("Entering invalid password")
        password_input = driver.find_element(By.CSS_SELECTOR, 'input[name="password"]')
        password_input.send_keys("P@ssword123")

        sign_in_button = driver.find_element(By.CSS_SELECTOR, 'form[action="/account/login"] button[type="submit"]')
        print("Clicking the Sign in button..")
        sign_in_button.click()
        time.sleep(10)
        
        error_notification = driver.find_element(By.CSS_SELECTOR, '[class^="mb-6"] p')
        assert error_notification.is_displayed(), "No Error Notification displayed"
        expected_message = "Sorry. We did not recognize either your email or password. Please try to sign in again or create a new account."
        assert expected_message == error_notification.text , "Expected Message is not correct"
        print("Error Message expected")
            
    def test_successful_login(self, driver) -> None:
        driver.refresh()
        print("\nVerify Successful login")
        login_section = driver.find_element(By.CSS_SELECTOR, 'main[class="relative grow"] div[class="mx-auto"]')  
        assert login_section.is_displayed(), "The login section is not displayed"
        print("Login section is displayed")

        # Input valid email
        print("Entering valid email")
        email_input = driver.find_element(By.CSS_SELECTOR, 'input[name="email"]')
        email_input.send_keys("lourdes@ecrubox.com")

        # Input valid password
        print("Entering valid password")
        password_input = driver.find_element(By.CSS_SELECTOR, 'input[name="password"]')
        password_input.send_keys("P@ssword1234")

        sign_in_button = driver.find_element(By.CSS_SELECTOR, 'form[action="/account/login"] button[type="submit"]')
        print("Clicking the Sign in immediately..") 
        sign_in_button.click()
        time.sleep(10)
        
        if driver.current_url == "https://www.varley.com/account":
            print("Login successful. URL is correct.")
        else:
            print(f"Login failed or wrong redirect. Current URL: {driver.current_url}")
            

if __name__ == "__main__":
    login_page = Test_Login_Page()
    login_page.test_nav_to_page("prod")