from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

import requests
import time

url = "https://www.varley.com/"


class Varley_Home_Page:    
    def test_nav_to_page(self, env) -> None:
        driver = self.setup_driver()
        url = "https://www.varley.com/"

        driver.get(url)
        time.sleep(2)
        
        self.verify_main_banner(driver)
        self.verify_category_carousel(driver)
        self.verify_third_block(driver)
        self.verify_fourth_block(driver)
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
    
    # Link: https://tuskr.live/project/1081dd66-4131-4537-a9e4-859653c572e7/test-case/ccb7944e-afe2-4875-a65f-e963d0217021
    # Test Case #: C-1
    def verify_main_banner(self, driver):
        print("Verifying the Main Hero Banner")
        # MAIN HERO
        expected_h1 = "Varley club."
        main_hero_text_element = driver.find_element(By.CSS_SELECTOR, "div.heroBannerContent h1").text.strip().replace("\ufeff", "")
        assert expected_h1 == main_hero_text_element, f"FAILED \n Expected text: '{expected_h1}' \n Got: '{main_hero_text_element}'"
        print("Main Text is expected - PASSED")

        expected_main_hero = "Discover our new Club Collection. Made to serve versatility whether you’re on the court or relaxing at the country club."
        main_hero_dec_element = driver.find_element(By.CSS_SELECTOR, "div.mt-1 p.text.text-body").text
        assert expected_main_hero == main_hero_dec_element, f"Expected text '{expected_h1}' but got '{main_hero_dec_element}'"
        print("Description is expected - PASSED")

        expected_button_link = "https://www.varley.com/collections/club"
        main_hero_button = driver.find_element(By.CSS_SELECTOR, "div.mt-7.inline-flex.flex-wrap a.uiButton")
        main_hero_button.click()
        WebDriverWait(driver, 20).until(EC.url_to_be(expected_button_link))

        current_url = driver.current_url

        # URL verification
        if current_url == expected_button_link:
            print("Expected link opened. Navigating back to the previous page.")
            driver.back()
            time.sleep(3)
        else:
            print("Different link opened:", current_url)

        # Image checking
        image = driver.find_element(By.CSS_SELECTOR, '#blocks\.heroBanner_663518e8690e4a34ae01a88f094b065a > div.relative.w-full > picture > img')
        image_url = image.get_attribute('src')
        response = requests.get(image_url)
                
        if response.status_code == 200:
            print("Image loaded successfully with status 200. - PASSED")
        else:
            print(f"Image {image_url} failed to load. Status code: {response.status_code}")

    # Link: https://tuskr.live/project/1081dd66-4131-4537-a9e4-859653c572e7/test-case/776bd08b-1761-4cfa-91a0-902dba0ac537
    # Test Case #: C-196
    def verify_category_carousel(self, driver):
        # 2nd Block (Category Carousel)
        collection_carousel_element = driver.find_element(By.CSS_SELECTOR, '[data-insider-id="blocks.carousel-2"]')
        driver.execute_script("arguments[0].scrollIntoView(true);", collection_carousel_element)
        driver.execute_script("window.scrollBy(0, -100);")

        time.sleep(3)
        print("Navigating to carousel block")
        expected_category_values = {
            "New Arrivals": "https://www.varley.com/collections/new-arrivals",
            "DoubleSoft®": "https://www.varley.com/collections/double-soft",
            "Sweaters & Knitwear": "https://www.varley.com/collections/knitwear-and-sweaters",
            "Outerwear": "https://www.varley.com/collections/outerwear",
            "Alpine": "https://www.varley.com/collections/alpine",
            "Pants": "https://www.varley.com/collections/pants",
            "Activewear": "https://www.varley.com/collections/activewear",
            "Sweatpants": "https://www.varley.com/collections/sweatpants"
        }

        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".slick-slide")))

        for category_name, expected_url in expected_category_values.items():
            index = list(expected_category_values.keys()).index(category_name)

            # Check if the current page needs navigation to the second carousel page
            if category_name in ["Alpine", "Activewear", "Pants", "Sweatpants"]:
                print("Clicking the button for page 2 to continue checking items.")
                button = driver.find_element(By.CSS_SELECTOR, ".slick-dots li:nth-child(2) button")
                button.click()
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, f"[data-index='4'].slick-active"))
                )
                print("Page 2 activated successfully.")
                print("-" * 50)

            try:
                element = driver.find_element(By.CSS_SELECTOR, f"[data-index='{index}']")
                if "slick-active" in element.get_attribute("class"):
                    print(f"{category_name} at index {index} is ACTIVE")

                    img = driver.find_element(By.CSS_SELECTOR, f"[data-index='{index}'] img")
                    # img_src = img.get_attribute('src')
                    # Image checking
                    is_loaded = driver.execute_script("return arguments[0].complete && arguments[0].naturalHeight > 0", img)
                    if is_loaded:
                        print(f"Image for {category_name} is loaded properly.")
                    else:
                        print(f"Image for {category_name} failed to load.")

                    # URL Verification
                    link = driver.find_element(By.CSS_SELECTOR, f"[data-index='{index}'] a")
                    href = link.get_attribute("href")

                    if href:
                        if expected_url == href:
                            print(f"URL for {category_name} ({href}) matches the expected URL.")
                        else:
                            print(f"URL for {category_name} ({href}) does NOT match the expected URL ({expected_url}).")

                        print(f"Navigating to {href}")
                        driver.execute_script("arguments[0].scrollIntoView(true);", link)
                        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, f"[data-index='{index}'] a")))
                        print(f"Clicking on link for {category_name}")
                        driver.execute_script("arguments[0].click();", link)
                        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
                        print(f"Navigation to link for {category_name} successful.")
                        driver.get(url)
                        WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.CLASS_NAME, "slick-slide"))
                        )
                        print("Carousel reloaded successfully.")
                        print("-" * 50)
                else:
                    print(f"{category_name} at index {index} is not ACTIVE")
            except Exception as e:
                print(f"Error processing {category_name} at index {index}: {e}")

    # Link: https://tuskr.live/project/1081dd66-4131-4537-a9e4-859653c572e7/test-case/069117a6-3ef4-4e1e-951d-f651ae5a20d4
    # Test Case #: C-197
    def verify_third_block(self,driver):
        # Verifying the 3rd block
        third_block_element = driver.find_element(By.CSS_SELECTOR , '[data-insider-id="blocks.split-3"]')
        driver.execute_script("arguments[0].scrollIntoView(true);", third_block_element)
        driver.execute_script("window.scrollBy(0, -100);")
        print("Navigated to 3rd block")
        time.sleep(3)
        
        expected_h3_texts = [
            "Light outer layers.",
            "New season DoubleSoft®."
        ]
        expected_links = {
            "Shop Jackets & Coats": "https://www.varley.com/collections/jackets-and-coats",
            "Shop Now": "https://www.varley.com/collections/double-soft"
        }

        print("Verify titles")
        h3_elements = third_block_element.find_elements(By.CSS_SELECTOR, "h3.title")
        h3_texts = [h3.get_attribute("innerText").strip().replace("\n", " ") for h3 in h3_elements]
        assert all(text in h3_texts for text in expected_h3_texts), f"Unexpected h3 text: {h3_texts}"

        print("\nVerify secondary text and links")
        links = third_block_element.find_elements(By.CSS_SELECTOR, ".mt-4 a")
        for link in links:
            text = link.text.strip()
            href = link.get_attribute("href")
            assert text in expected_links, f"Unexpected link text: {text}"
            assert href == expected_links[text], f"Incorrect URL for {text}: {href}"
            print(f"{text} link is correct: {href} ")

        print("\nVerify images")
        image_elements = third_block_element.find_elements(By.CSS_SELECTOR, "picture img")
        for img in image_elements:
            img_src = img.get_attribute("src")
            response = requests.head(img_src)
            assert response.status_code == 200, f"Image {img_src} returned {response.status_code}"
        print("Images are not broken")
    
    def verify_fourth_block(self,driver):
        # Verifying the 4th block
        fourth_block_element = driver.find_element(By.CSS_SELECTOR , '[data-insider-id="blocks.split-4"]')
        driver.execute_script("arguments[0].scrollIntoView(true);", fourth_block_element)
        driver.execute_script("window.scrollBy(0, -100);")
        print("Navigated to 3rd block")
        time.sleep(3)
        
        expected_h3_texts = [
            "Transitional knits.",
            "Visit us in-store."
        ]
        expected_links = {
            "Shop Now": "https://www.varley.com/collections/knitwear-and-sweaters",
            "Explore Now": "https://www.varley.com/pages/our-stores"
        }

        print("Verify titles")
        h3_elements = fourth_block_element.find_elements(By.CSS_SELECTOR, "h3.title")
        h3_texts = [h3.get_attribute("innerText").strip().replace("\n", " ") for h3 in h3_elements]
        assert all(text in h3_texts for text in expected_h3_texts), f"Unexpected h3 text: {h3_texts}"

        print("\nVerify secondary text and links")
        links = fourth_block_element.find_elements(By.CSS_SELECTOR, ".mt-4 a")
        for link in links:
            text = link.text.strip()
            href = link.get_attribute("href")
            assert text in expected_links, f"Unexpected link text: {text}"
            assert href == expected_links[text], f"Incorrect URL for {text}: {href}"
            print(f"{text} link is correct: {href} ")

        print("\nVerify images")
        image_elements = fourth_block_element.find_elements(By.CSS_SELECTOR, "picture img")
        for img in image_elements:
            img_src = img.get_attribute("src")
            response = requests.head(img_src)
            assert response.status_code == 200, f"Image {img_src} returned {response.status_code}"
        print("Images are not broken")

if __name__ == "__main__":
    varley_home_page = Varley_Home_Page()
    varley_home_page.test_nav_to_page("prod")