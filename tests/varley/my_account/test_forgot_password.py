import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

class Test_Forgot_Password:   
    def test_nav_to_page(self, env) -> None:
        driver = self.setup_driver()
        url = "https://www.varley.com/account/login"
        driver.get(url)
        time.sleep(2)
        
        self.verify_location_modal(driver)
        self.test_nav_to_forgot_password(driver)
        self.text_validate_elements(driver)
        self.test_validate_email(driver)
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
    
    def test_nav_to_forgot_password(self, driver) -> None:
        print("\nNavigate to Forgot Password Page from Login")
        
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "email"))
        )

        forgot_password_link = driver.find_element(By.LINK_TEXT, "Forgot password?")
        forgot_password_link.click()

        WebDriverWait(driver, 10).until(EC.url_contains("/account/recover"))
        current_url = driver.current_url

        if current_url.startswith("https://www.varley.com/account/recover"):
            print("Successfully redirected to Forgot Password page:", current_url)
        else:
            print("Failed to redirect. Current URL:", current_url)
            
    def text_validate_elements(self,driver) -> None:
        container = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '[class*="max-w-[546px]"]'))
        )

        print("Recover Password section is visible")
        header = container.find_element(By.TAG_NAME, "h1").text.strip()
        assert header == "Recover password", f" Unexpected header text: {header}"
        print("Header text is correct")

        subtext = container.find_element(By.TAG_NAME, "p").text.strip()
        expected_subtext = "Enter your email address to receive a password reset link."
        assert subtext == expected_subtext, f"Unexpected subtext: {subtext}"
        print("✅ Subtext is correct")

        label = container.find_element(By.XPATH, ".//label[@for='email']").text.strip()
        assert label == "Email address", f"Unexpected label: {label}"
        print("✅ Email label is correct")

        cancel_button = container.find_element(By.LINK_TEXT, "Cancel")
        reset_button = container.find_element(By.XPATH, ".//button[@type='submit']")

        assert cancel_button.is_displayed(), "Cancel button not found"
        assert reset_button.text.strip() == "Send reset link", f"Reset button text mismatch: {reset_button.text}"
        print("Cancel and Send reset link buttons are displayed correctly")
    
    def test_validate_email(self, driver) -> None:
        wait = WebDriverWait(driver, 10)

        email_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input#email")))
        send_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")

        print("\nTestValidate empty field")
        email_input.clear()
        print("Click Submit button immediately")
        send_button.click()

        error_message = wait.until(EC.presence_of_element_located((
            By.CSS_SELECTOR,
            "div.text-red.border-red p"
        )))
        assert "Please provide an email." in error_message.text
        print("Empty email test passed")
        
        print("\nTest invalid emails")
        invalid_emails = [
            "test@",              # missing domain
            "@email.com",         # missing local part
            "testemail.com",      # missing @
        ]

        for email in invalid_emails:
            email_input.clear()
            email_input.send_keys(email)
            send_button.click()

            error = wait.until(EC.presence_of_element_located((
                By.CSS_SELECTOR, "div.mt-2.text-sm.text-red"
            )))

            assert "Invalid email address" in error.text
            print(f"Error for '{email}': {error.text}")
            time.sleep(1)

        print("\nTest valid emails")
        valid_email = "lourdes@ecrubox.com"
        email_input.clear()
        email_input.send_keys(valid_email)
        print("Clicking the submit button")
        send_button.click()
        time.sleep(3)

        confirmation_container = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "main#mainContent h1"))
        )

        heading_text = confirmation_container.text.strip()
        assert heading_text == "Recover password", f"Unexpected heading: {heading_text}"
        print("Heading text is verified")

        success_message = driver.find_element(By.CSS_SELECTOR, "main#mainContent .text-sm > p")
        expected_snippet = "you’ll receive an email with instructions"
        assert expected_snippet in success_message.text.strip(), f"Unexpected message: {success_message.text.strip()}"
        print("Success Message is verified")
        
        back_to_signin_btn = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "a[href='/account/login'].text-white"))
        )

        button_text = back_to_signin_btn.text.strip()
        assert "Back to sign in" in button_text, "'Back to sign in' button missing or incorrect"
        print("Back to sign in button is verified")
        
if __name__ == "__main__":
    forgot_password_page = Test_Forgot_Password()
    forgot_password_page.test_nav_to_page("prod")