import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


class Test_Gift_Card_Page:
    def test_nav_to_page(self, env) -> None:
        driver = self.setup_driver()
        url = "https://www.varley.com/products/e-gift-card"

        driver.get(url)
        time.sleep(2)
        self.verify_location_modal(driver)
        self.verify_that_the_page_is_viewable(driver)
        self.test_content(driver)
        self.test_sending_to_myself(driver)
        self.test_sending_to_someone_else_future_date(driver)
        self.test_add_all_denomination(driver)
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
            EC.presence_of_element_located((By.CSS_SELECTOR, '[id="headlessui-dialog-panel-:r2:"]'))
        )
        if geoip_modal.is_displayed():
            print("GeoIP modal is visible")
            close_button = geoip_modal.find_element(By.CSS_SELECTOR, '[aria-label="Close Country Select"]')
            print("Clicking the close button on the GeoIP modal")
            close_button.click()
            time.sleep(2)
            print("GeoIP modal is now hidden. Continuing with the test")
        else:
            print("GeoIP modal is hidden. Continuing with the test.")
        
    def verify_that_the_page_is_viewable(self, driver) -> None:
        print("Breadcrumbs is displayed")
        time.sleep(5)
        
        breadcrumbs = [item.text for item in driver.find_elements(By.CSS_SELECTOR, "nav ul li a")]
        print(f"Breadcrumbs: {' / '.join(breadcrumbs)}")

        homepage_link = driver.find_element(By.CSS_SELECTOR, 'a[href="/"]')
        home_page = homepage_link.get_attribute("href")
        if not home_page.startswith("http"):
            home_page = "https://www.varley.com" + home_page

        gift_edit_link = driver.find_element(By.CSS_SELECTOR, 'a[href="/collections/gift-edit"]')
        gift_edit = gift_edit_link.get_attribute("href")
        if not gift_edit.startswith("http"):
            gift_edit = "https://www.varley.com" + gift_edit

        expected_homepage_link = "https://www.varley.com/"
        expected_gift_edit_link = "https://www.varley.com/collections/gift-edit"

        assert home_page == expected_homepage_link, f"Homepage link is incorrect. Expected: {expected_homepage_link}, Actual: {home_page}"
        assert gift_edit == expected_gift_edit_link, f"Gift Edit link is incorrect. Expected: {expected_gift_edit_link}, Actual: {gift_edit}"

        print(f"Homepage link correct: {home_page}")
        print(f"Gift Edit link correct: {gift_edit}\n")
        
    def test_content(self, driver) -> None:
        print("Test Content")

        test_results = {
            "h1": "E-Gift Card",
            "description": "Give the gift of choice with a Varley e-gift card.",
            "h4": "E-gift card value:",
            "select_label": "Select amount",
            "dropdown_amounts": ["$50", "$100", "$150", "$200", "$250", "$500"],
            "note": "Please note: E-gift cards are non-refundable and cannot be applied to existing orders. Items purchased with e-gift cards follow our regular returns and exchanges policy.",
            "who_are_you_gifting_text": "Who are you gifting?"
        }
        
        title = driver.find_element(By.CSS_SELECTOR, ".font-plantin h1")  
        assert title.text == test_results["h1"], "Title is incorrect"
        print("Title is correct")
        
        description = driver.find_element(By.CSS_SELECTOR, 'p[class="mt-\[24px\] text-sm"]')
        assert description.text == test_results["description"], "Description is incorrect"
        print("Description is correct")
        
        gift_card_value = driver.find_element(By.CSS_SELECTOR, 'h4[class="pb-\[18px\] font-medium"]')
        assert gift_card_value.text == test_results["h4"], "Gift Card Value text is incorrect"
        print("Gift Card Value is correct")
        
        select_amount_text = driver.find_element(By.CSS_SELECTOR, 'p[class="pb-\[18px\] text-sm"]')
        assert select_amount_text.text == test_results["select_label"], "Select Amount text is incorrect"
        print("Select Amount text is correct")
        
        options = [opt.text for opt in driver.find_elements(By.TAG_NAME, "option")]
        print(f"Options: {', '.join(options)}")     
        assert options == test_results["dropdown_amounts"], "Dropdown amounts are incorrect"
        print("Dropdown amounts are correct")
        
        who_are_you_gifting = driver.find_element(By.CSS_SELECTOR, '[class~="giftCardForm"] h4')
        driver.execute_script("arguments[0].scrollIntoView(true);", who_are_you_gifting)
        time.sleep(2)
        assert who_are_you_gifting.is_displayed(), "'Who Are You Gifting' element is not displayed"
        print("Who Are You Gifting element is displayed")
        
        who_are_you_gifting_text: str = who_are_you_gifting.text
        assert who_are_you_gifting_text == test_results["who_are_you_gifting_text"], f"who_are_you_gifting_text is incorrect. Actual:\n {who_are_you_gifting_text} Expected:\n{test_results['who_are_you_gifting_text']}"
        print("who_are_you_gifting_text is correct\n")
        
        note = driver.find_element(By.CSS_SELECTOR, 'p[class~="mt-[20px]"]')
        driver.execute_script("arguments[0].scrollIntoView(true);", note)
        time.sleep(2)
        assert note.is_displayed(), "Note is not displayed"
        print("Note is displayed")
        
        note_text: str = note.text
        assert note_text == test_results["note"], f"Note is incorrect. Actual:\n {note_text} Expected:\n{test_results['note']}"
        print("Note is correct\n")
        
        print("Verify if Someone Else button is selected by default")
        selected_span = driver.find_element(
            By.CSS_SELECTOR, 
            "div.recipient-type div:nth-child(2) span"
        )
        selected_class = selected_span.get_attribute("class")
        assert "bg-black text-white" in selected_class, "Someone Else button is not selected by default"
        print("Someone Else button is selected by default\n")        
        
        print("Verify image is displayed and not broken")
        print("Verify the main product image")
        main_product_image = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'img[class="aspect-[3/4] object-cover"]'))
        )
        assert main_product_image.is_displayed(), "Image is not visible"
        img_src = main_product_image.get_attribute("src")
        response = requests.get(img_src)
        status_code = response.status_code
        assert status_code == 200, "Product Image is broken"
        print("Main Product Image is NOT broken and visible\n")
        
        thumbnail_image = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'img[class="h-auto w-full object-cover"]'))
        )
        assert thumbnail_image.is_displayed(), "Image is not visible"
        img_src = main_product_image.get_attribute("src")
        response = requests.get(img_src)
        status_code = response.status_code
        assert status_code == 200, "Thumbnail Image is broken"
        print("Thumbnail Image is NOT broken and visible\n")
        
        # zoom_icon = WebDriverWait(driver, 10).until(
        #     EC.presence_of_element_located((By.CSS_SELECTOR, '[class="relative flex-1"] span[class^="absolute"] svg'))
        # )
        # assert zoom_icon.is_displayed(), "Zoom Icon is not visible"
        # print("Zoom icon is displayed. Clicking the zoom icon")
        # driver.execute_script("arguments[0].scrollIntoView();", zoom_icon)

        # zoom_icon.click()
        # print("Zoom icon is clicked")
        # time.sleep(5)
        # image_slide_show = WebDriverWait(driver, 10).until(
        #     EC.presence_of_element_located((By.CSS_SELECTOR, '[class*="yarl__fullsize"]'))
        # )
        # assert image_slide_show.is_displayed(), "Image slideshow is not visible after clicking zoom icon"
        # print("Image slide show is shown")
        
        # print("Verify if the image in the slide show is not broken")
        # time.sleep(3)
        # zoom_image = WebDriverWait(image_slide_show, 10).until(
        #     EC.presence_of_element_located((By.CSS_SELECTOR, 'img'))
        # )
        # img_src = zoom_image.get_attribute("src")
        # response = requests.get(img_src)
        # status_code = response.status_code
        # assert status_code == 200, "Zoom Image is broken"
        # print("Zoom Image is NOT broken and visible\n")
        
        # print("Closing the zoom screen")
        # close_yarl = WebDriverWait(driver, 10).until(
        #     EC.presence_of_element_located((By.CSS_SELECTOR, '[class="yarl__button"]'))
        # )
        # close_yarl.click
        # time.sleep(3)
        # print("Zoom screen is closed")
        
    def test_sending_to_someone_else_future_date(self, driver) -> None:
        print("\nVerify that I can add a gift card to my cart and send it to someone else with a future date")

        someone_else_button = driver.find_element(By.XPATH, "//span[contains(text(), 'Someone Else')]")
        
        print("Select 'Someone Else' and check if form is visible")
        someone_else_button.click()
        time.sleep(1)
        
        form = driver.find_element(By.CSS_SELECTOR, '[class="mt-\[48px\] flex flex-col"]') 
        if form.is_displayed():
            print("Form is visible when 'Someone Else' is selected")
            driver.execute_script("arguments[0].scrollIntoView(true);", form)

            print("\nAdding Information")
            recipientName = "Des Test"
            recipientEmail = "lourdes@ecrubox.com"
            confirmRecipientEmail = "lourdes@ecrubox.com"
            message = "Test message"
            senderName = "Ecrubox"
            sendOn = "05-25-2025"
            
            form.find_element(By.NAME, "recipientName").send_keys(recipientName)
            print(f"Recipient's Name: {recipientName}")
            time.sleep(1)
            form.find_element(By.NAME, "recipientEmail").send_keys(recipientEmail)
            print(f"Recipient's Name: {recipientEmail}")
            time.sleep(1)
            form.find_element(By.NAME, "confirmRecipientEmail").send_keys(confirmRecipientEmail)
            print(f"Recipient's Email: {confirmRecipientEmail}")
            time.sleep(1)
            form.find_element(By.NAME, "message").send_keys(message)
            print(f"Message: {message}")
            time.sleep(1)
            form.find_element(By.NAME, "senderName").send_keys(senderName)
            print(f"Sender's Name: {senderName}")
            time.sleep(1)
            driver.find_element(By.CSS_SELECTOR, "input[name='sendNow'][value='false']").click()
            time.sleep(1)
            date_field = driver.find_element(By.NAME, "sendOn")
            if date_field.is_displayed():
                date_field.send_keys(sendOn)
                print(f"Date is set to {sendOn}")
            time.sleep(1)
            add_to_bag_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Add to bag')]"))
                )
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
            product_image = product_container.find_element(By.CSS_SELECTOR, "img[alt='$50']")
            assert product_image.is_displayed(), "Image is not visible"
            
            img_src = product_image.get_attribute("src")
            response = requests.get(img_src)
            status_code = response.status_code
            assert status_code == 200, "Product Image is broken"
            print("Product Image is NOT broken and visible")
            
            # Verify product name
            expected_product_name: str = "E-Gift Card"
            product_name = WebDriverWait(product_container, 10).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, "a.font-plantin"))
                )
            product_name_text = product_name.text
            assert product_name_text == expected_product_name, f"Expected 'E-Gift Card' but found '{product_name_text}'"
            print(f"Product name is displayed in the cart: {product_name_text}")
            
            # Verify the price
            expected_price: str = "$50.00"
            price = WebDriverWait(product_container, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "div.mt-2.tracking-wider > span"))
            )
            price_text = price.text
            assert price_text == expected_price, f"Expected '$50.00' but found '{price_text}'"
            print(f"Product Price is displayed in the cart: {price_text}")

            # Verify quantity
            expected_quantity = "1"
            quantity = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'text-normal') and contains(@class, 'flex')]"))
            )
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
        
    def test_sending_to_myself(self, driver) -> None:
        print("\nVerifying the 'Myself' variant and check if form is hidden")
        myself_btn = driver.find_element(By.CSS_SELECTOR, '.bg-black:nth-child(1)')
        driver.execute_script("arguments[0].scrollIntoView(true);", myself_btn)
        driver.execute_script("window.scrollBy(0, -300);")
        time.sleep(3)
        print("Clicking the Myself button")
        myself_btn.click()
        time.sleep(3)
        driver.execute_script("arguments[0].click();", myself_btn)

        add_to_bag_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Add to cart')]"))
                )
        add_to_bag_button.click()
        time.sleep(3)
        print("Clicked the Add to bag button")
        
        side_cart = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "div.side-cart[data-headlessui-state='open']"))
        )
        assert side_cart.is_displayed(), "Side cart is not displayed after clicking the Add to bag button"
        print("Side Cart is displayed. \nVerifying the Side Cart item")
        time.sleep(20)
        
        product_container = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div[role='table'][aria-label='Shopping cart'] div[role='row']:not(.sr-only)"))
        )
        # Verify image
        product_image = product_container.find_element(By.CSS_SELECTOR, "img[alt='$50']")
        assert product_image.is_displayed(), "Image is not visible"
        
        img_src = product_image.get_attribute("src")
        response = requests.get(img_src)
        status_code = response.status_code
        assert status_code == 200, "Product Image is broken"
        print("Product Image is NOT broken and visible")
        
        # Verify product name
        expected_product_name: str = "E-Gift Card"
        product_name = WebDriverWait(product_container, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "a.font-plantin"))
            )
        product_name_text = product_name.text
        assert product_name_text == expected_product_name, f"Expected 'E-Gift Card' but found '{product_name_text}'"
        print(f"Product name is displayed in the cart: {product_name_text}")
        
        # Verify the price
        expected_price: str = "$50.00"
        price = WebDriverWait(product_container, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "div.mt-2.tracking-wider > span"))
        )
        price_text = price.text
        assert price_text == expected_price, f"Expected '$50.00' but found '{price_text}'"
        print(f"Product Price is displayed in the cart: {price_text}")

        # Verify quantity
        expected_quantity = "1"
        quantity = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'text-normal') and contains(@class, 'flex')]"))
        )
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
    
    def test_add_all_denomination(self, driver) -> None:
        print("\nVerifying all denomination can be added to cart")
        myself_button = driver.find_element(By.XPATH, "//span[contains(text(), 'Myself')]")
        driver.execute_script("arguments[0].click();", myself_button)
        print("Clicking the Myself button")
        time.sleep(3)
        driver.execute_script("window.scrollBy(0, -100);")
        
        dropdown = driver.find_element(By.NAME, "selectedVariantId")
        options = dropdown.find_elements(By.TAG_NAME, "option")

        for denomination in options:
            amount = denomination.text
            
            denomination.click()
            print(f"Selected denomination: {amount}")
            time.sleep(2)
            
            myself_button = driver.find_element(By.XPATH, "//span[contains(text(), 'Myself')]")
            driver.execute_script("arguments[0].click();", myself_button)
            print("Clicked Myself button")
            time.sleep(2)
            
            driver.execute_script("window.scrollBy(0, -100);")
            add_to_cart = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Add to cart')]"))
            )
            add_to_cart.click()
            print(f"Added {amount} to cart")
            time.sleep(3)
            
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
            product_image = product_container.find_element(By.CSS_SELECTOR, f"img[alt='{amount}']")
            assert product_image.is_displayed(), "Image is not visible"
            print(f"Product Image for {amount} is displayed")
            
            img_src = product_image.get_attribute("src")
            response = requests.get(img_src)
            status_code = response.status_code
            assert status_code == 200, "Product Image is broken"
            print("Product Image is NOT broken and visible")
            
            # Verify product name
            expected_product_name: str = "E-Gift Card"
            product_name = WebDriverWait(product_container, 10).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, "a.font-plantin"))
                )
            product_name_text = product_name.text
            assert product_name_text == expected_product_name, f"Expected 'E-Gift Card' but found '{product_name_text}'"
            print(f"Product name is displayed in the cart: {product_name_text}")
            
            # Verify the price
            price = WebDriverWait(product_container, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "div.mt-2.tracking-wider > span"))
            ).text
            print(f"Product Price is displayed in the cart: {price}")

            # Verify quantity
            expected_quantity = "1"
            quantity = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'text-normal') and contains(@class, 'flex')]"))
            )
            quantity_text = quantity.text
            assert quantity_text == expected_quantity, f"Expected quantity '1' but found '{quantity_text}'"
            print(f"Product QTY is displayed in the cart: {quantity_text}")
            
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

        print("Finished adding and verifying all denominations to cart")
        
if __name__ == "__main__":
    gift_card_page = Test_Gift_Card_Page()
    gift_card_page.test_nav_to_page("prod")