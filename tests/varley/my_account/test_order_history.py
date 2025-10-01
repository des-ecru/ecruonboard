import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

class Test_Order_History:   
    def test_nav_to_page(self, env) -> None:
        driver = self.setup_driver()
        url = "https://www.varley.com/account/login"
        driver.get(url)
        time.sleep(2)
        
        self.test_location_modal(driver)
        self.test_verify_log_in(driver)
        self.test_navigate_order_history(driver)
        self.test_order_history(driver)
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
    
    def test_location_modal(self, driver) -> None:
        print("Location Modal Test")
        time.sleep(2)
        geoip_modal = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '[id^="headlessui-dialog-panel"]'))
        )
        if geoip_modal.is_displayed():
            print("GeoIP modal is visible")
            close_button = geoip_modal.find_element(By.CSS_SELECTOR, 'svg.cursor-pointer')
            close_button.click()
            time.sleep(2)
            print("GeoIP modal is now closed. Continuing with the test\n")
        else:
            print("GeoIP modal is closed. Continuing with test.\n")
            
    def test_verify_log_in(self, driver) -> None:
    
        print("Entering valid email")
        email_input = driver.find_element(By.CSS_SELECTOR, 'input[name="email"]')
        email_input.send_keys("lourdes@ecrubox.com")

        print("Entering valid password")
        password_input = driver.find_element(By.CSS_SELECTOR, 'input[name="password"]')
        password_input.send_keys("P@ssword123")

        sign_in_button = driver.find_element(By.CSS_SELECTOR, 'form[action="/account/login"] button[type="submit"]')
        print("Clicking the Sign in immediately..") 
        sign_in_button.click()
        time.sleep(5)
        
        if driver.current_url == "https://www.varley.com/account":
            print("Login successful. URL is correct.")
            print("Customer is in the account page")
        else:
            print(f"Login failed or wrong redirect. Current URL: {driver.current_url}")
            
    def test_navigate_order_history(self, driver) -> None:
        order_history_locator = (
            By.CSS_SELECTOR, 
            'a[data-discover="true"][href="/account/orders"]'
        )
        order_history_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(order_history_locator)
        )
        order_history_link.click()
        print("Clicked the 'Order history' link.")

    def test_order_history(self, driver) -> None:
        last_6_months_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, r'button.flex.w-\[160px\].cursor-pointer.items-center.border.bg-white.px-5.py-4'))
        )
        label_span = last_6_months_button.find_element(By.CSS_SELECTOR, 'span.mr-auto.text-sm')
        if label_span.text.strip() == "Last 6 months":
            print("Clicking 'Last 6 months' button...")
            last_6_months_button.click()
        else:
            print(f"Found button but label is '{label_span.text.strip()}', not 'Last 6 months'.")

        last_3_months_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((
                By.XPATH, 
                "//button[contains(@class, 'flex') and contains(@class, 'items-center') and contains(text(), 'Last 3 months')]"
            ))
        )
        print("Clicking 'Last 3 months' button...")
        last_3_months_button.click()
        time.sleep(2)

        self.populate_order(driver, section='last 3 months')

        time.sleep(3)

        self.populate_order(driver, section='last 6 months')
        
        driver.execute_script("window.scrollTo(0, 0);")
        button_locator = (
            By.XPATH,
            "//button[contains(@class, 'flex') and contains(@class, 'cursor-pointer') and .//span[text()='Last 6 months']]"
        )
        button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(button_locator)
        )

        button.click()
        print("Clicked the 'Last 6 months' button.")
        button_locator = (
            By.XPATH,
            "//button[contains(@class, 'flex') and contains(@class, 'items-center') and contains(@class, 'overflow-hidden') and contains(@class, 'py-1') and contains(@class, 'text-sm') and contains(@class, 'hover:opacity-80') and normalize-space(text())='2025']"
        )
        button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(button_locator)
        )

        button.click()
        print("Clicked the '2025' button.")
        time.sleep(5)

        self.populate_order(driver, '2025')

    def populate_order(self, driver, section=''):
        activer_order = 0
        orders_count = 0
        while True:
            container_locator = (By.CSS_SELECTOR, "div.flex.items-center.justify-center.gap-6")
            container = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(container_locator)
            )
            buttons = container.find_elements(By.TAG_NAME, "button")
            if len(buttons) >= 2:
                second_button = buttons[1] 
                is_visible = second_button.is_displayed()
                is_enabled = second_button.is_enabled()
                print(f"Second button visible: {is_visible}")
                print(f"Second button enabled (clickable): {is_enabled}")
                if is_visible and is_enabled:
                    print("Second button is clickable!")
                else:
                    print("Second button is NOT clickable.")
            else:
                print(f"Only found {len(buttons)} button(s) inside the container. No second button available.")
            order_items = driver.find_elements(By.CSS_SELECTOR, 'li.flex.flex-col.flex-wrap.items-start.justify-between.gap-y-3.border.border-\\[\\#C7BFB9\\].bg-white.p-6')
            
            view_order_link = order_items[activer_order].find_element(By.CSS_SELECTOR, 'a.text-sm.underline[data-discover="true"]')
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable(view_order_link))
            view_order_link.click()
            print(f"Clicked 'View order' for order {activer_order}")
            time.sleep(5)

            parent_container_locator = (By.CSS_SELECTOR, "div.flex-grow.p-5.pb-15.pt-10.md\\:p-10.lg\\:p-20.lg\\:pb-20.lg\\:pt-20")
            parent_container = driver.find_element(*parent_container_locator)
            child_product_locator = "div.flex.gap-4.pb-6.md\\:gap-16.md\\:border-b.md\\:border-\\[\\#C7BFB9\\].md\\:pt-6.xl\\:gap-x-32"
            product_children = parent_container.find_elements(By.CSS_SELECTOR, child_product_locator)
            print(f"Found {len(product_children)} product item(s).")

            for index, product in enumerate(product_children, 1):
                dt_elements = product.find_elements(By.TAG_NAME, "dt")
                if dt_elements:
                    item_name = dt_elements[0].text.strip()
                else:
                    item_name = "<No item name found>"

                a_tags = product.find_elements(By.CSS_SELECTOR, "a[data-discover='true']")
                if a_tags:
                    images = a_tags[0].find_elements(By.TAG_NAME, "img")
                    has_image = len(images) > 0
                else:
                    has_image = False

                print(f"Product {index}: Name = '{item_name}', Has image = {has_image}")

            activer_order += 1
            driver.back()
            time.sleep(2)
            if activer_order == len(order_items):
                break

            if section == 'last 3 months':
                last_6_months_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.flex.w-\[160px\].cursor-pointer.items-center.border.bg-white.px-5.py-4'))
                )
                label_span = last_6_months_button.find_element(By.CSS_SELECTOR, 'span.mr-auto.text-sm')
                if label_span.text.strip() == "Last 6 months":
                    print("Clicking 'Last 6 months' button...\n")
                    last_6_months_button.click()
                else:
                    print(f"Found button but label is '{label_span.text.strip()}', not 'Last 6 months'.\n")
                last_3_months_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((
                        By.XPATH, 
                        "//button[contains(@class, 'flex') and contains(@class, 'items-center') and contains(text(), 'Last 3 months')]"
                    ))
                )
                print("Clicking 'Last 3 months' button...\n")
                last_3_months_button.click()
                time.sleep(2)
            
            if section == '2025':
                driver.switch_to.default_content()
                driver.execute_script("window.scrollTo(0, 0);")
                button_locator = (
                    By.XPATH,
                    "//button[contains(@class, 'flex') and contains(@class, 'cursor-pointer') and .//span[text()='Last 6 months']]"
                )
                button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable(button_locator)
                )

                button.click()
                print("Clicked the 'Last 6 months' button.")

                # XPath locator matching the button by class and exact text "2025"
                button_locator = (
                    By.XPATH,
                    "//button[contains(@class, 'flex') and contains(@class, 'items-center') and contains(@class, 'overflow-hidden') and contains(@class, 'py-1') and contains(@class, 'text-sm') and contains(@class, 'hover:opacity-80') and normalize-space(text())='2025']"
                )
                button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable(button_locator)
                )

                button.click()
                print("Clicked the '2025' button.")
                time.sleep(5)

            if activer_order == len(order_items):
                # Locator for the container div
                container_locator = (By.CSS_SELECTOR, "div.flex.items-center.justify-center.gap-6")
                container = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located(container_locator)
                )
                buttons = container.find_elements(By.TAG_NAME, "button")
                if len(buttons) >= 2:
                    second_button = buttons[1] 
                    is_visible = second_button.is_displayed()
                    is_enabled = second_button.is_enabled()
                    print(f"Second button visible: {is_visible}")
                    print(f"Second button enabled (clickable): {is_enabled}")
                    if is_visible and is_enabled:
                        print("Second button is clickable!")
                    else:
                        print("Second button is NOT clickable.")
                else:
                    print(f"Only found {len(buttons)} button(s) inside the container. No second button available.")

                driver.execute_script("window.scrollBy(0, 200);")
                time.sleep(5)
                second_button.click()
                activer_order = 0
                time.sleep(5)
            
    def is_element_present(self, driver, locator):
        return len(driver.find_elements(*locator)) > 0
 
if __name__ == "__main__":
    order_history = Test_Order_History()
    order_history.test_nav_to_page("prod")