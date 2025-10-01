
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


class Test_Product_Page:   
    def test_nav_to_page(self, env) -> None:
        driver = self.setup_driver()
        # url = "https://www.varley.com/products/scott-scoop-neck-midi-dress?variant=44489831219373&color=Birch&size=XXS"
        url = "https://www.varley.com/products/alana-slim-tapered-cuff-pant-29?variant=44372758266029&color=Simply%20Taupe&size=XXS"
        driver.get(url)
        time.sleep(2)
        self.verify_location_modal(driver)
        self.verify_that_the_page_is_viewable(driver)
        self.test_content(driver)
        self.test_content_accordion(driver)
        self.test_add_to_cart(driver)
        self.test_complete_the_look(driver)
        
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
            close_button = geoip_modal.find_element(By.CSS_SELECTOR, '#headlessui-dialog-title-\:r1\: > svg')
            
            close_button.click()
            time.sleep(2)
            print("GeoIP modal is now hidden. Continuing with the test")
        else:
            print("GeoIP modal is hidden. Continuing with test.")
        
    def verify_that_the_page_is_viewable(self, driver) -> None:
        print("Breadcrumbs is displayed")
        time.sleep(5)
        
        breadcrumbs = [item.text for item in driver.find_elements(By.CSS_SELECTOR, "nav ul li a")]
        print(f"Breadcrumbs: {' / '.join(breadcrumbs)}")

        homepage_link = driver.find_element(By.CSS_SELECTOR, 'a[href="/"]')
        home_page = homepage_link.get_attribute("href")
        if not home_page.startswith("http"):
            home_page = "https://www.varley.com" + home_page

        collection_breadcrumbs = driver.find_element(By.CSS_SELECTOR, 'a[href="/collections/knitwear-and-sweaters"]')
        collection_link = collection_breadcrumbs.get_attribute("href")
        if not collection_link.startswith("http"):
            collection_link = "https://www.varley.com" + collection_link

        expected_homepage_link = "https://www.varley.com/"
        expected_collection_link = "https://www.varley.com/collections/knitwear-and-sweaters"

        assert home_page == expected_homepage_link, f"Homepage link is incorrect. Expected: {expected_homepage_link}, Actual: {home_page}"
        assert collection_link == expected_collection_link, f"Collection Breadcrumb link is incorrect. Expected: {expected_collection_link}, Actual: {collection_link}"

        print(f"Homepage Breadcrumb link correct: {home_page}")
        print(f"Collection Breadcrumb link correct: {collection_link}\n")
        
    def test_content(self, driver) -> None:
        print("Product Content")
        title = driver.find_element(By.CSS_SELECTOR, ".text-\[19px\]\/\[22px\]")  
        assert title.is_displayed(), "Title is not displayed"
        # assert title.text == test_results["h1"], "Title is incorrect"
        print("Title is correct")
        
        description = driver.find_element(By.CSS_SELECTOR, '.px-5 > .mb-5')
        assert description.is_displayed(), "Description is displayed"
        # assert description.text == test_results["description"], "Description is incorrect"
        print("Description is not correct")
        
        product_price = driver.find_element(By.CSS_SELECTOR, '.px-5 > .text-black')
        assert product_price.is_displayed(), "Product Price is not displayed"
        print("Product Price is correct")
        
        color_text = driver.find_element(By.CSS_SELECTOR, '.items-center > .block')
        assert color_text.is_displayed(), "Color text label is not displayed"
        print("Color text label is displayed\n")
        
        color_section = driver.find_element(By.CSS_SELECTOR, '.gap-6 > .flex:nth-child(2)')
        color_buttons = color_section.find_elements(By.CSS_SELECTOR, 'div.flex.flex-wrap.gap-3 button')
        total_colors = len(color_buttons)
        assert total_colors > 0, "No color buttons found"
        print(f"\nFound {total_colors} color options")

        for index in range(total_colors):
            print(f"\nClicking color button #{index + 1}")
            color_section = driver.find_element(By.CSS_SELECTOR, '.gap-6 > .flex:nth-child(2)')
            color_buttons = color_section.find_elements(By.CSS_SELECTOR, 'div.flex.flex-wrap.gap-3 button')

            btn = color_buttons[index]
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
            driver.execute_script("arguments[0].click();", btn)
            time.sleep(3)

            label_element = color_section.find_element(By.CSS_SELECTOR, 'span.block')
            label_text = label_element.text.strip()

            assert label_text.startswith("Color:"), f"Unexpected label format: {label_text}"
            selected_color = label_text.replace("Color:", "").strip()

            print(f"Confirmed: '{selected_color}' is selected")
        
        print("\nVerifying the size chart link")
        size_chart_link = driver.find_element(By.CSS_SELECTOR, '.underline-offset-4:nth-child(2)')
        assert size_chart_link.is_displayed(), "Size Chart is not displayed"
        print("Size Chart is displayed")
        print("Clicking the Size Chart link")
        size_chart_link.click()
        time.sleep(2)
        size_guide_modal = driver.find_element(By.CSS_SELECTOR, 'div[data-headlessui-state="open"]')
        assert size_guide_modal.is_displayed(), "Size Guide modal is not displayed"
        print("Size Guide modal is displayed")
        print("Closing the Size Guide modal")
        close_button = size_guide_modal.find_element(By.CSS_SELECTOR, 'svg[class*="cursor-pointer"]')
        close_button.click()
        
        WebDriverWait(driver, 10).until(
            EC.invisibility_of_element_located((By.CSS_SELECTOR, 'div[data-headlessui-state="open"]'))
        )
        print("Size Guide modal is closed\n")
        
        print("Verifying the size variant")
        container = driver.find_element(By.CSS_SELECTOR, 'div.flex.border.border-black')
        buttons = container.find_elements(By.TAG_NAME, 'button')

        available_sizes = [btn.text.strip() for btn in buttons]
        print(f"Available sizes: {available_sizes}")

        for size_text in available_sizes:
            print(f"Clicking size: {size_text}")
            container = driver.find_element(By.CSS_SELECTOR, 'div.flex.border.border-black')
            buttons = container.find_elements(By.TAG_NAME, 'button')

            # Find the button matching the current size label
            btn_to_click = next((btn for btn in buttons if btn.text.strip() == size_text), None)
            assert btn_to_click, f"Button with text '{size_text}' not found"
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn_to_click)
            driver.execute_script("arguments[0].click();", btn_to_click)
            time.sleep(3)

            container = driver.find_element(By.CSS_SELECTOR, 'div.flex.border.border-black')
            buttons = container.find_elements(By.TAG_NAME, 'button')
            selected_buttons = [btn.text.strip() for btn in buttons if "bg-black" in btn.get_attribute("class")]

            assert selected_buttons == [size_text], f"Expected selected size '{size_text}', but got: {selected_buttons}"
            print(f"Confirmed: {size_text} is selected")
    

        print(f"\nVerifying the Delivery Note")
        delivery_note_text = driver.find_element(By.CSS_SELECTOR, "div.my-10 p")
        assert delivery_note_text.is_displayed(), "Delivery Note is not displayed"
        print("Delivery Note is displayed")
        delivery_note = delivery_note_text.text.replace("/br"," ").strip()
        expected_delivery_note_text = "Free delivery on U.S. orders over $100\nFree U.S. returns for 30 days"
        assert delivery_note == expected_delivery_note_text, f"Expected delivery note text is incorrect. Got: {delivery_note}"
        print(f"{expected_delivery_note_text}")
    
    def test_content_accordion(self,driver) -> None:
        description_accordion = driver.find_element(By.CSS_SELECTOR, '[class^="px-5"] [class="overflow-hidden"]:nth-child(6)')
        driver.execute_script("arguments[0].scrollIntoView();", description_accordion)
        driver.execute_script("window.scrollBy(0, -100);")
        assert description_accordion.is_displayed(), "Description accordion is not displayed"
        print("Description accordion is displayed")
        description_accordion.click()
        time.sleep(3)
        description_content = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".gap-4:nth-child(1)"))
        )
        print(f"Description: {description_content.text.strip()}")
        
        print("\nVerify Fit & Measurement")
        fit_measurement_button = driver.find_element(By.XPATH, "//button[contains(., 'Fit & Measurements')]")
        driver.execute_script("arguments[0].click();", fit_measurement_button)
        fit_measurement_content_panel = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//button[contains(., 'Fit & Measurements')]/following-sibling::div"))
        )
        assert fit_measurement_content_panel.is_displayed(), "Fit & Measurements accordion is not displayed"
        fit_measurement_full_text = fit_measurement_content_panel.text.strip()
        print(f"Fit & Measurements:\n{fit_measurement_full_text}")
        
        print("\nVerify Fabric & Care")
        fabric_care_button = driver.find_element(By.XPATH, "//button[contains(., 'Fabric & Care')]")
        driver.execute_script("arguments[0].click();", fabric_care_button)
        fabric_care_content_panel = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//button[contains(., 'Fabric & Care')]/following-sibling::div"))
        )
        assert fabric_care_content_panel.is_displayed(), "Fabric & Care accordion is not displayed"
        fabric_care_full_text = fabric_care_content_panel.text.strip()
        print(f"Fabric & Care text:\n{fabric_care_full_text}")
        
        print("\nVerify Delivery & Returns")
        delivery_return_button = driver.find_element(By.XPATH, "//button[contains(., 'Delivery & Returns')]")
        driver.execute_script("arguments[0].click();", delivery_return_button)
        delivery_return_content_panel = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//button[contains(., 'Delivery & Returns')]/following-sibling::div"))
        )
        assert delivery_return_content_panel.is_displayed(), "Fabric & Care accordion is not displayed"
        delivery_return_full_text = delivery_return_content_panel.text.strip()
        print(f"Delivery & Returns text:\n{delivery_return_full_text}")
    
    def test_add_to_cart(self,driver) -> None:
        print("\nSelecting a size and adding it to cart")
        
        add_to_bag_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".h-\\[42px\\]"))
        )
        driver.execute_script("arguments[0].scrollIntoView();", add_to_bag_button)
        driver.execute_script("window.scrollBy(0, -100);")
        add_to_bag_button.click()
        time.sleep(3)
        print("Clicked the Add to bag button")
        
        sidecart = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "div.side-cart[data-headlessui-state='open']"))
        )
        assert sidecart.is_displayed(), "Side cart is not displayed after clicking the Add to bag button"
        print("Side Cart is displayed. \nVerifying the Side Cart item")
        time.sleep(20)
        
        product_container = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div[role='table'][aria-label='Shopping cart'] div[role='row']:not(.sr-only)"))
        )
        # Verify image
        product_image = product_container.find_element(By.CSS_SELECTOR, ".mr-5 img")
        assert product_image.is_displayed(), "Image is not visible"
        
        img_src = product_image.get_attribute("src")
        response = requests.get(img_src)
        status_code = response.status_code
        assert status_code == 200, "Product Image is broken"
        print("Product Image is NOT broken and visible")
        
        # Verify product name
        product_name = WebDriverWait(product_container, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "a.font-plantin"))
            )
        assert product_name.is_displayed(), "Product name is not visible"
        product_name_text = product_name.text
        print(f"Product name is displayed in the cart: {product_name_text}")
        
        # Verify the price
        price = WebDriverWait(product_container, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "div.mt-2.tracking-wider > span"))
        )
        assert price.is_displayed(), "Price is not visible"
        price_text = price.text
        print(f"Product Price is displayed in the cart: {price_text}")

        # Verify quantity
        expected_quantity = "1"
        quantity = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'text-normal') and contains(@class, 'flex')]"))
        )
        assert quantity.is_displayed(), "Quantity is not visible"
        quantity_text = quantity.text
        assert quantity_text == expected_quantity, f"Expected quantity '1' but found '{quantity_text}'"
        print(f"Product is displayed in the cart: {quantity_text}")
            
        close_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.side-cart[data-headlessui-state="open"] button.outline-none'))
        )
        close_button.click()
        time.sleep(3)
        print("Clicked the close button")
        WebDriverWait(driver, 10).until(
            EC.invisibility_of_element_located((By.CSS_SELECTOR, 'div.side-cart[data-headlessui-state="open"]'))
        )
        print("Sidecart is closed\n")
        
    def test_complete_the_look(self, driver)-> None:
        print("\nVerfiying the Complete the look section")
        complete_the_look = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '[class^="px-5"] [class="overflow-hidden"]:nth-child(8) button'))
        )
        driver.execute_script("arguments[0].scrollIntoView();", complete_the_look)
        driver.execute_script("window.scrollBy(0, -100);")
        
        assert complete_the_look.is_displayed(), "Complete the look section is not displayed"
        print("Complete the Look section is displayed")
        
        print("\nClick the Quick Preview button")
        quick_preview_selector = 'button.absolute.right-0.top-0.z-\\[2\\]'

        initial_buttons = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, quick_preview_selector))
        )
        print(f"Found {len(initial_buttons)} Quick Preview button(s)")

        for idx in range(len(initial_buttons)):
            quick_preview_buttons = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, quick_preview_selector))
            )
            button = quick_preview_buttons[idx]

            assert button.is_enabled(), f"\nQuick Preview button #{idx} is not enabled"
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", button)
            time.sleep(0.5)

            driver.execute_script("arguments[0].click();", button)
            time.sleep(1.5)

            quick_preview_modal = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, '[class^="quickshop__main"]'))
            )
            assert quick_preview_modal.is_displayed(), "Quick Preview modal is not displayed"
            print(f"Quick Preview modal for product #{idx+1} is displayed")

if __name__ == "__main__":
    product_page = Test_Product_Page()
    product_page.test_nav_to_page("prod")