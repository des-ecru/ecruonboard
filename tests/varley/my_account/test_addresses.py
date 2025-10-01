import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


class Test_Addresses:
    def test_nav_to_page(self) -> None:
        driver = self.setup_driver()
        url = "https://www.varley.com/account/login"
        driver.get(url)
        time.sleep(2)
        
        self.verify_location_modal(driver)
        self.test_verify_log_in(driver)
        self.test_nav_to_address_book(driver)
        self.test_add_test_address(driver)
        self.test_login_with_new_account(driver)
        self.test_navigate_order_history(driver)
        driver.quit()
    
    def setup_driver(self):
        print("Setting up Chrome driver...")
        chrome_options = Options()
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-popup-blocking")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--start-maximized")
        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        print("Driver setup complete.")
        return driver

    def verify_location_modal(self, driver):
        print("Checking for location modal...")
        modals = driver.find_elements(By.CSS_SELECTOR, '[id^="headlessui-dialog-panel"]')
        if modals and modals[0].is_displayed():
            print("Location modal detected, closing it...")
            close_button = modals[0].find_element(By.CSS_SELECTOR, 'svg.cursor-pointer')
            close_button.click()
            WebDriverWait(driver, 10).until(EC.invisibility_of_element(modals[0]))
            print("Modal closed successfully.")

    def test_verify_log_in(self, driver):

        email_in = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[name="email"]'))
        )
        email_in.clear()
        email_in.send_keys("lourdes@ecrubox.com")

        pwd_in = driver.find_element(By.CSS_SELECTOR, 'input[name="password"]')
        pwd_in.clear()
        pwd_in.send_keys("P@ssword123")

        sign_in_btn = driver.find_element(By.CSS_SELECTOR, 'form[action="/account/login"] button[type="submit"]')
        sign_in_btn.click()

        WebDriverWait(driver, 20).until(EC.url_to_be("https://www.varley.com/account"))
        print("Login successful.")
    
    def test_nav_to_address_book(self, driver):
        print("Navigating to Address Book...")
        addr_link = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[href="/account/addresses"]'))
        )
        addr_link.click()
        WebDriverWait(driver, 20).until(EC.url_contains("/account/addresses"))
        print("Now at:", driver.current_url)
    
    def test_add_test_address(self, driver):
        print("Clicking Add Address button...")
        add_btn = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[href="/account/address/add"]'))
        )
        add_btn.click()

        WebDriverWait(driver, 20).until(EC.url_contains("/account/address/add"))
        print("Now at (Add Address):", driver.current_url)

        test_data = {
            "firstName": "Test First",
            "lastName": "Test Last",
            "address1": "123 Test Street",
            "city": "Testville",
            "zip": "TST123",
            "phone": "+44 7777 777769"
        }

        for field, value in test_data.items():
            print(f"Filling {field}...")
            input_el = WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, f'input[name="{field}"]'))
            )
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", input_el)
            input_el.clear()
            input_el.send_keys(value)
            time.sleep(0.5)

        # self.close_location_modal(driver)

        save_btn = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable(
                (By.XPATH, '//button[@type="submit" and contains(normalize-space(.), "Save address")]')
            )
        )
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", save_btn)
        print("Clicking Save address button...")
        save_btn.click()

        WebDriverWait(driver, 20).until(EC.url_contains("/account/addresses"))
        print("Redirected to address book page, address saved successfully!")

        # self.set_latest_address_as_default(driver)

        # default_block = self.locate_latest_address(driver)
        # self.edit_this_address(driver, default_block)

        # self.delete_default_address(driver)






    def locate_latest_address(self, driver):
        print("Locating the latest (newest) address block...")
        address_css = "div.relative.flex.flex-col.border"
        WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, address_css))
        )
        addresses = driver.find_elements(By.CSS_SELECTOR, address_css)
        latest_address = addresses[-1]
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", latest_address)
        print("Found and scrolled to latest address.")
        return latest_address

    def set_latest_address_as_default(self, driver):
        print("Setting the latest address as default...")
        latest_address = self.locate_latest_address(driver)
        form = latest_address.find_element(By.CSS_SELECTOR, "form.flex.items-center")
        label = form.find_element(By.XPATH, './/label[contains(text(), "Set as default address")]')
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", label)
        time.sleep(1)
        print("Clicking 'Set as default address'...")
        label.click()
        time.sleep(3)
        print("New address set as default successfully.")

    def edit_this_address(self, driver, address_block):
        print("Editing the newly set default address...")

        edit_btn = WebDriverWait(address_block, 20).until(
            lambda block: block.find_element(
                By.XPATH, './/a[.//span[contains(text(),"Edit delivery address")]]'
            )
        )
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", edit_btn)
        edit_btn.click()

        WebDriverWait(driver, 20).until(EC.url_contains("/account/address"))
        print("Now at the Edit Address page.")

        edit_data = {
            "firstName": "Edited",
            "lastName": "Default",
            "company": "Varley Clothing Ltd",
            "address1": "456 Changed Street",
            "city": "Los Angeles",
            "province": "CA",
            "zip": "90001",
            "phone": "+1 310-555-1234"
        }

        for field, value in edit_data.items():
            print(f"Editing field {field}...")
            input_el = WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, f'input[name="{field}"]'))
            )
            input_el.clear()
            input_el.send_keys(value)
            time.sleep(0.5)

        country_select = Select(driver.find_element(By.CSS_SELECTOR, 'select[name="country"]'))
        country_select.select_by_visible_text("United States")
        print("Country set to United States.")

        update_btn = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable(
                (By.XPATH, '//button[@type="submit" and (contains(text(), "Update address") or contains(text(), "Save address"))]')
            )
        )
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", update_btn)
        print("Clicking Update address button...")
        update_btn.click()

        WebDriverWait(driver, 20).until(EC.url_contains("/account/addresses"))
        print("Default Address successfully edited!")

    def delete_default_address(self, driver):
        print("Attempting to delete the default address...")

        address_blocks = driver.find_elements(By.CSS_SELECTOR, "div.relative.flex.flex-col.border")
        default_block = None

        for block in address_blocks:
            labels = block.find_elements(By.XPATH, './/p[contains(text(),"Default Address")]')
            if labels and labels[0].is_displayed():
                default_block = block
                break

        if not default_block:
            print("No Default Address block found, ending test.")
            self.finalize_test(driver)
            return

        delete_btn = WebDriverWait(default_block, 20).until(
            lambda b: b.find_element(By.XPATH, './/span[contains(text(),"Delete address")]')
        )
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", delete_btn)
        print("Clicking Delete address button...")
        delete_btn.click()

        confirm_btn = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable(
                (By.XPATH, '//div[contains(@class,"bg-white")]//button[contains(text(),"Confirm")]')
            )
        )
        print("Clicking Confirm button in delete modal...")
        confirm_btn.click()
        time.sleep(2)

        x_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, 'svg.absolute.right-\\[30px\\].top-\\[30px\\].cursor-pointer')
            )
        )
        print("Clicking the X button to close modal...")
        x_button.click()
        time.sleep(1)

        print("Default Address deleted and modal closed successfully!")
        self.finalize_test(driver)

    
    

if __name__ == "__main__":
    address = Test_Addresses()
    address.test_nav_to_page()
