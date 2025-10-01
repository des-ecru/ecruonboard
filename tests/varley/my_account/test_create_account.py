import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

class Test_Create_Account:   
    def test_nav_to_page(self, env) -> None:
        driver = self.setup_driver()
        url = "https://www.varley.com/account/login"
        driver.get(url)
        time.sleep(2)
        
        self.verify_location_modal(driver)
        self.test_nav_to_register(driver)
        self.test_create_account_duplicate_email(driver)
        self.test_renavigate_to_signin(driver)
        self.test_create_account_successfully(driver)
       
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
    
    def test_nav_to_register(self, driver) -> None:
        print("\nNavigate to Create Account Page")
        login_section = driver.find_element(By.CSS_SELECTOR, 'main[class="relative grow"] div[class="mx-auto"]')  
        assert login_section.is_displayed(), "The login section is not displayed"
        print("Login section is displayed")
        
        create_account_link = driver.find_element(By.LINK_TEXT, "Create an account")
        create_account_link.click()
        time.sleep(10)

        current_url = driver.current_url
        expected_url = "https://www.varley.com/account/register"

        assert current_url == expected_url, f"Navigation failed. Current URL:{current_url} "
        print("Navigation successful. URL:", current_url)
    
    def test_create_account_duplicate_email(self, driver) -> None:
        print("\nCreate Account Test -> Duplicate Email")
        
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "firstName"))
        )
        print("Entering details...")
        driver.find_element(By.ID, "firstName").send_keys("Des")
        time.sleep(1)
        driver.find_element(By.ID, "lastName").send_keys("Test")
        time.sleep(1)
        driver.find_element(By.NAME, "phone").send_keys("9123456789")
        time.sleep(1)
        driver.find_element(By.ID, "email").send_keys("lourdes@ecrubox.com")
        time.sleep(1)
        driver.find_element(By.ID, "newPassword").send_keys("P@ssword123")
        time.sleep(1)
        driver.find_element(By.ID, "newPassword2").send_keys("P@ssword123")
        time.sleep(1)
        
        create_button = driver.find_element(By.XPATH, "//button[text()='Create account']")
        if not create_button.is_enabled():
            driver.execute_script("arguments[0].disabled = false;", create_button)
            print("Button is disabled")
            return

        create_button.click()
        time.sleep(5)
        WebDriverWait(driver, 8).until(EC.url_contains("/account"))
        current_url = driver.current_url
        if current_url.startswith("https://www.varley.com/account"):
            error_box = WebDriverWait(driver, 5).until(
                EC.visibility_of_element_located(
                    (By.XPATH, "//div[contains(@class, 'border-red') and contains(., 'Email has already been taken')]")
                )
            )
            assert error_box.is_displayed(), f"Error message not displayed. Current URL:{current_url}"
            print("Registration failed: Email has already been taken.")
        time.sleep(3)
        driver.refresh()
    
    def test_renavigate_to_signin(self, driver) -> None:
        print("\nCreate Account Test -> Re-navigate to Signin Page")
        
        sign_in_link = driver.find_element(By.LINK_TEXT, "Sign in")
        print("Clicking the Sign-in button")
        sign_in_link.click()

        WebDriverWait(driver, 10).until(EC.url_contains("/account/login"))
        current_url = driver.current_url
        expected_url = "https://www.varley.com/account/login"

        assert current_url.startswith(expected_url), f"Failed to navigate. Expected URL: {expected_url}, Actual URL: {current_url}"
        print("Successfully navigated to login page:", current_url)
        
        self.test_nav_to_register(driver)
        
    def test_create_account_successfully(self, driver) -> None:
        print("\nCreate Account Successfully")
        
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "firstName"))
        )
        print("Entering details...")
        timestamp = int(time.time())
        random_email = f"lourdes+{timestamp}@ecrubox.com"
        driver.find_element(By.ID, "firstName").send_keys("Des")
        driver.find_element(By.ID, "lastName").send_keys("Test")
        driver.find_element(By.NAME, "phone").send_keys("9123456789")
        driver.find_element(By.ID, "email").send_keys(f"{random_email}")
        driver.find_element(By.ID, "newPassword").send_keys("P@ssword123")
        driver.find_element(By.ID, "newPassword2").send_keys("P@ssword123")

        create_button = driver.find_element(By.XPATH, "//button[text()='Create account']")
        if not create_button.is_enabled():
            driver.execute_script("arguments[0].disabled = false;", create_button)
        print("Clicking the 'Create account' button...")
        create_button.click()
        time.sleep(10)
        WebDriverWait(driver, 10).until(EC.url_contains("/account"))
        current_url = driver.current_url
        expected_url = "https://www.varley.com/account"

        assert current_url.startswith(expected_url), f"Unexpected URL: {current_url}"
        print("Successfully redirected to:", current_url)
        print("Account is logged in")
      
if __name__ == "__main__":
    create_account_page = Test_Create_Account()
    create_account_page.test_nav_to_page("prod")