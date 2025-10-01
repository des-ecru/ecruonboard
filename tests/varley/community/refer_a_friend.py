
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager



class Varley_Refer_A_Friend:    
    def test_nav_to_page(self, env) -> None:
        driver = self.setup_driver()
        url = "https://www.varley.com/pages/refer-a-friend"

        driver.get(url)
        time.sleep(2)
        # self.verify_location_modal(driver)
        self.verify_that_the_page_is_viewable(driver)
        self.verify_refer_a_friend(driver)
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
        print("Verifying if Location modal appears")
        location_modal = driver.find_element(By.CSS_SELECTOR, "div[id^='headlessui-dialog-panel']")
        if location_modal.is_displayed():
            print("Location modal is displayed")
            cancel_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//button[contains(@class, 'uiButton') and contains(text(), 'Cancel')]"))
            )
            cancel_button.click()
            print("Clicking the Cancel button to close\n")
            time.sleep(2)

    def verify_that_the_page_is_viewable(self, driver) -> None:
        print("Verify Referral Page\n")
        image_element = driver.find_element(By.CSS_SELECTOR, '.yotpo-left-align-image')
        image_url = image_element.get_attribute('src')
        response = requests.get(image_url)
        assert response.status_code == 200, f"The image returned a status code of {response.status_code}."
        print("The image on the right is not broken")
             
    def verify_refer_a_friend(self, driver) -> None:
        print("\nVerify Content block")
        expected_output = [
            "Refer a",
            "Give 15% off, get 15% off.",
            "Refer your friends to Varley and they'll get 15% off their first purchase. As a thank you, you'll also receive 15% off."
        ]

        header_text = driver.find_element(By.CSS_SELECTOR, '.yotpo-header-text').text
        title_text = driver.find_element(By.CSS_SELECTOR, '#yotpoReferralTitleText').text
        description_text = driver.find_element(By.CSS_SELECTOR, '#yotpoReferralDescriptionText').text

        actual_output = [header_text, title_text, description_text]
        assert actual_output == expected_output, "Incorrect text displayed" 
        print("The text on the webpage matches the expected output.\n")
        
        print("Input referral details")
        name = "QA Ecrubox"
        email = "lourdes@ecrubox.com"
        friends_email = "giyacuvox@gmail.com"

        driver.find_element(By.CSS_SELECTOR, '#first-name').send_keys(name)
        print(f"Your Name: {name}")

        driver.find_element(By.CSS_SELECTOR, 'input[placeholder="Enter your email address"]').send_keys(email)  
        print(f"Your Email Address: {email}")          
        
        next_button = driver.find_element(By.CSS_SELECTOR, '.yotpo-button-style.yotpo-button-standard-size.yotpo-filled-button.yotpo-rectangular-btn-type')
        print("Clicking the Next button\n")
        next_button.click()
        time.sleep(3)
        print("Customer is directed to next screen\n")
        print("Clicking the referral link")
        copy_button = driver.find_element(By.CSS_SELECTOR, ".yotpo-widget-copy-link-container .yotpo-copy-link")
        copy_button.click()
        
        # need help to get the referral url
        # link = driver.execute_script("""
        #     return arguments[0].getAttribute('data-url') || 
        #         arguments[0].closest('[data-url]')?.getAttribute('data-url') || 
        #         window.location.href;
        # """, copy_button)
        # print("Copied Link:", link)

        self.handle_share_button(driver, ".yotpo-twitter-share-button", "x.com", "twitter")
        self.handle_share_button(driver, ".yotpo-facebook-share-button", "facebook.com/dialog", "facebook")
        self.handle_share_button(driver, ".yotpo-facebook-messenger-share-button", "facebook.com", "facebook messenger")
        self.handle_share_button(driver, ".yotpo-whatsapp-share-button", "api.whatsapp.com", "whatsapp")

        driver.find_element(By.CSS_SELECTOR, 'input[placeholder="Enter your friend’s email address"]').send_keys(friends_email)  
        print(f"Friend's email: {friends_email}")        
        
        send_referral_button = driver.find_element(By.CSS_SELECTOR, '.yotpo-button-style.yotpo-button-standard-size.yotpo-filled-button.yotpo-rectangular-btn-type')
        print("Clicking the Send Referral button\n")
        send_referral_button.click()
        time.sleep(3)
        
        expected_thank_you_text = "for referring"
        thank_you_element = driver.find_element(By.CSS_SELECTOR, ".yotpo-header-text")
        assert expected_thank_you_text in thank_you_element.text, "Thank you text is incorrect or missing."
        print("Thank you text is correctly displayed")

        expected_reminder_text = "Remind your friends to check their emails."
        reminder_element = driver.find_element(By.CSS_SELECTOR, ".yotpo-title-text")
        assert expected_reminder_text in reminder_element.text, "Reminder text is incorrect or missing."
        print("Reminder text is correctly displayed")

        expected_button_text = "Refer another friend"
        button_element = driver.find_element(By.CSS_SELECTOR, ".yopto-widget-button-text")
        assert expected_button_text in button_element.text, "Button text is incorrect or missing."
        print(f"CTA button text is changed to {expected_button_text}\n")
        print("All expected texts are displayed correctly.")
        
        print("\nVerify if friend's email is displayed on the referral list")
        driver.find_element(By.XPATH, "//div[contains(text(), 'Your referrals')]").click()
        time.sleep(3)

        friend_email_element = driver.find_element(By.CSS_SELECTOR, ".yotpo-row-left-text")
        assert friends_email in friend_email_element.text, "Friend's email is not displayed."

        print("Friend's email is displayed correctly.")
    
    def handle_share_button(self, driver, selector, expected_url, social_network):
        main_window = driver.current_window_handle
        driver.find_element(By.CSS_SELECTOR, selector).click()
        time.sleep(2)

        new_window = None
        for handle in driver.window_handles:
            if handle != main_window:
                new_window = handle
                break

        if new_window:
            driver.switch_to.window(new_window)
            # print(f"Opened: {driver.current_url}")
            time.sleep(3)

            assert expected_url in driver.current_url, f"{expected_url} for {social_network} is not expected!"
            print(f"Window for {social_network} appear!")
            time.sleep(3)
            driver.close()
            driver.switch_to.window(main_window)

if __name__ == "__main__":
    varley_refer_a_friend_page = Varley_Refer_A_Friend()
    varley_refer_a_friend_page.test_nav_to_page("prod")
