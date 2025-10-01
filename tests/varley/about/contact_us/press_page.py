from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import requests

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException


class Press_Page:    
    def test_nav_to_page(self, env) -> None:
        driver = self.setup_driver()
        url = "https://www.varley.com/pages/press"

        driver.get(url)
        time.sleep(2)
        
        self.verify_location_modal(driver)
        self.verify_header_footer(driver)
        self.verify_breadcrumbs(driver)
        self.verify_main_hero(driver)
        self.verify_submission_of_form_with_empty_details(driver)
        self.verify_successful_submission_of_form(driver)
      
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

    def verify_location_modal(self, driver):
        print("Verifying if Location modal appear")
        location_modal = driver.find_element(By.CSS_SELECTOR, "div[id^='headlessui-dialog-panel']")
        if location_modal.is_displayed():
            print("Location modal is displayed")
            
            cancel_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//button[contains(@class, 'uiButton') and contains(text(), 'Cancel')]"))
                )
            cancel_button.click()
            print("Clicking the Cancel button to close")
            time.sleep(2)
        else:
            print("Location modal is not displayed")
    
    def verify_header_footer(self, driver):
        print("Verify if header and footer exists")
        header = driver.find_element(By.CSS_SELECTOR, "header")
        if header.is_displayed():
            print("Header exists in Wholesale Page")
        footer = driver.find_element(By.CSS_SELECTOR, "footer")
        if footer.is_displayed():
            print("Footer exists in Wholesale Page")
        
    def verify_breadcrumbs(self, driver):
        breadcrumbs_container = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".mx-auto.max-w-\[1558px\]"))
        )
        print("Breadcrumbs is displayed")

        breadcrumbs_items = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "ol.flex li.text-brandAsphalt"))
        )

        for item in breadcrumbs_items:
            name = item.text.strip()
            print(name)

            link_element = item.find_elements(By.CSS_SELECTOR, "a")
            if link_element:
                href = link_element[0].get_attribute("href")
                print(f"Link: {href}")
                assert href == "https://www.varley.com/", "Home breadcrumb does not have the expected link!"

    def verify_main_hero(self, driver):
        print("\nVerify the Main hero Banner")
        hero_banner = driver.find_element(By.CSS_SELECTOR, ".hero.relative")
        print("Hero banner is present.")

        print("Verify the main hero banner image")
        image_element = hero_banner.find_element(By.CSS_SELECTOR, ".image-wrap img")
        image_url = image_element.get_attribute("src")
        response = requests.get(image_url)
        assert response.status_code == 200, f"Hero image failed to load. Status Code: {response.status_code}"
        print("Hero image loaded successfully (200 OK).")

        print("Verify the title")
        title_element = hero_banner.find_element(By.CSS_SELECTOR, "h1")
        title_text = title_element.text.strip()
        assert title_text == "Press", f"Title verification failed. Found: '{title_text}'"
        print(f"Title verification passed: '{title_text}'")
        
        expected_content = (
            "For any press queries please contact us at marketing@varley.com "
            "Alternatively, leave your contact information below and we’ll get back to you as soon as we can. "
            "Please note we are not open on holidays or weekends. If you contact us after business hours, we will aim to get back to you the following business day."
        )

        content = driver.find_element(By.CSS_SELECTOR, ".py-10")  
        actual_text = content.text.strip() 

        print(f"Content:\n{actual_text}")

        normalized_expected = " ".join(expected_content.split()).strip()
        normalized_actual = " ".join(actual_text.split()).strip()

        assert normalized_expected == normalized_actual, f"Mismatch Found!\nExpected:\n{normalized_expected}\n\nActual:\n{normalized_actual}"
       
        email_link = driver.find_element(By.CSS_SELECTOR, "a[href^='mailto:']").get_attribute("href")
        assert "marketing@varley.com" in email_link, f"Email link mismatch! Found: {email_link}"
        print("\nEmail link is verified")

   
    def verify_submission_of_form_with_empty_details(self, driver):
        
        print("\nVerify Newsletter > clicking submit with empty email")
        submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        submit_button.click()
        time.sleep(1)
        try:
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, "div[data-role='error']")
                )
            )
            print("Empty field validation failed.")
        except TimeoutException:
            print("Empty field validation - PASSED.")
        
    def verify_successful_submission_of_form(self, driver):
        print("\nVerify the Successful Submission of Form")

        print("\nFilling out the form ")
        driver.find_element(By.CSS_SELECTOR, "input[name='name']").send_keys("Des Ecrubox")
        driver.find_element(By.CSS_SELECTOR, "input[name='email']").send_keys("lourdes@ecrubox.com")
        driver.find_element(By.CSS_SELECTOR, "textarea[name='message']").send_keys("This is a test message. Please ignore. (Automation Test)")
        time.sleep(2)
        print("Clicking the Submit")
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(5)

        print("Verify if the success message is displayed")
        success_message = driver.find_element(By.XPATH, "//div[contains(@class, 'flex') and contains(@class, 'gap-') and contains(@class, 'border-l-4') and contains(@class, 'border-s-') and contains(@class, 'bg-') and contains(@class, 'p-')]").text
        if "Thank you." in success_message and "We will respond within 2-5 business days." in success_message:
            print("Success message appears correctly.")
        else:
            print("Success message is missing or incorrect.")

        # Check button text
        button_text = driver.find_element(By.CSS_SELECTOR, "button.uiButton.bg-black").text.strip()
        if button_text == "Submit another enquiry":
            print("Button text is correct.")
        else:
            print(f"Button text incorrect: {button_text}")
            
            
if __name__ == "__main__":
    press_page = Press_Page()
    press_page.test_nav_to_page("prod")
