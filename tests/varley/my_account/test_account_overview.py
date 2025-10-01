import time 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException


password = "P@ssword123"

class Test_Account_Overview:   
    def test_nav_to_page(self) -> None:
        driver = self.setup_driver()
        url = "https://www.varley.com/account/login"
        driver.get(url)
        time.sleep(2)
        
        self.verify_location_modal(driver)
        self.test_verify_log_in(driver)
        self.test_verify_account_content(driver)
        self.test_edit_profile(driver)
        self.test_login_with_new_account(driver)
        self.test_navigate_order_history(driver)
        driver.quit()
    
    def setup_driver(self):
        chrome_options = Options()
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-popup-blocking")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--start-maximized")
        chrome_service = ChromeService(ChromeDriverManager().install())
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
            
    def test_verify_log_in(self, driver) -> None:
        time.sleep(10)
        print("Entering initial credentials...")
        email_input = driver.find_element(By.CSS_SELECTOR, 'input[name="email"]')
        print("Entering the e-mail address")
        email_input.send_keys("lourdes@ecrubox.com")
        password_input = driver.find_element(By.CSS_SELECTOR, 'input[name="password"]')
        print("Entering the password")
        password_input.send_keys(f"{password}")

        try:
            incorrect_password = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div.mb-6'))
            )
            print("Incorrect password detected, retrying...")
            
            # Retry with second password
            password_input = driver.find_element(By.ID, "CustomerPassword")
            password_input.clear()
            password_input.send_keys("P@ssword1234")
            sign_in_button = driver.find_element(By.CSS_SELECTOR, 'form[action="/account/login"] button[type="submit"]')
            sign_in_button.click()
            time.sleep(8)

        except TimeoutException:
            print("No incorrect password message found. Assuming login might have succeeded.")

        sign_in_button = driver.find_element(By.CSS_SELECTOR, 'form[action="/account/login"] button[type="submit"]')
        sign_in_button.click()
        time.sleep(8)
        assert "account" in driver.current_url,"Login failed"
        print("Login successful\n")
        time.sleep(3)
            
    def test_verify_account_content(self, driver):
        expected_account_text = "Account overview"
        expected_recent_text = "Recent orders"
        
        account_overview_block = WebDriverWait(driver, 25).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div.mb-15.flex.flex-col.gap-6.border'))
        )
        assert account_overview_block.is_displayed(), "Account content is not visible"
        print("Account Overview is displayed")
        
        account_title = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//h1[contains(text(), "Account overview")]'))
        )
        assert account_title.text.strip() == expected_account_text, f"Expected text: {expected_account_text}, Actual text: {account_title.text}"
        print("Account overview title is correct\n")

        account_overview_block = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div.mb-15.flex.flex-col.gap-6.border'))
        )
        assert account_overview_block.is_displayed(), "Account content is not visible"
        print("Account Overview block is displayed")
        recent_orders_title = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//h1[contains(text(), "Recent orders")]'))
        )
        assert recent_orders_title.text.strip() == expected_recent_text, f"Expected text: {expected_recent_text}, Actual text: {recent_orders_title.text}"
        print("Recent Orders title is correct")

    def test_edit_profile(self, driver) -> None:
        print("Navigating to Edit Profile page...")
        edit_profile_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[href="/account/edit"]'))
        )
        print("Clicking the Edit profile link")
        edit_profile_link.click()
        time.sleep(3)

        update_profile_form = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'form.max-w-\[572px\]'))
        )
        assert update_profile_form.is_displayed(), "Update Profile form is not visible"
        print("Update Profile form is displayed")

        print("Editing profile...")
        timestamp = int(time.time())
        firs_name = f"Des{timestamp}"
        first_name_input = update_profile_form.find_element(By.CSS_SELECTOR, 'input[name="firstName"]')
        first_name_input.clear()
        first_name_input.send_keys(f"{firs_name}")

        last_name_input = update_profile_form.find_element(By.CSS_SELECTOR, 'input[name="lastName"]')
        last_name_input.clear()
        last_name_input.send_keys("Ecrubox")

        # Set NEW password
        new_password_input = update_profile_form.find_element(By.CSS_SELECTOR, 'input[name="newPassword"]')
        new_password2_input = update_profile_form.find_element(By.CSS_SELECTOR, 'input[name="newPassword2"]')
        new_password_input.send_keys(f"{password}")
        new_password2_input.send_keys(f"{password}")

        save_button = update_profile_form.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
        save_button.click()
        time.sleep(8)
        print("Profile saved, redirected to Sign In page.\n")

    def test_login_with_new_account(self, driver) -> None:
        print("Logging in again with NEW password...")
        form = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'form[action="/account/login"]'))
        )

        email_input = form.find_element(By.CSS_SELECTOR, 'input[name="email"]')
        email_input.send_keys("lourdes@ecrubox.com")

        password_input = form.find_element(By.CSS_SELECTOR, 'input[name="password"]')
        password_input.send_keys(f"{password}")

        sign_in_button = form.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
        sign_in_button.click()
        time.sleep(8)

        assert "account" in driver.current_url, "Re-login failed."
        print("Successfully logged in with NEW credentials.")
    
    def test_navigate_order_history(self, driver) -> None:
        print("\nClick the order history menu")
        order_history_locator = (
            By.CSS_SELECTOR, 
            'a[data-discover="true"][href="/account/orders"]'
        )
        order_history_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(order_history_locator)
        )
        order_history_link.click()
        print("Clicked the 'Order history' link.")
        time.sleep(5)

if __name__ == "__main__":
    account_overview = Test_Account_Overview()
    account_overview.test_nav_to_page()