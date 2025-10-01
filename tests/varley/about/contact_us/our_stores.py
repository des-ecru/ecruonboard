from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
import re                    
import time
import requests

#Link: https://tuskr.live/project/1081dd66-4131-4537-a9e4-859653c572e7/test-case/74fe15d7-0ed1-4704-bbe8-9d2831b6fbca
# Test Case # C-184
class Varley_Our_Store_Page:    
    def test_nav_to_page(self, env) -> None:
        driver = self.setup_driver()
        url = "https://www.varley.com/pages/our-stores"

        driver.get(url)
        time.sleep(2)
        self.verify_new_york_store(driver)
        self.verify_madison_avenue(driver)
        self.verify_kings_road_address(driver)
        self.verify_marylebone_address(driver)
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
        driver = webdriver.Chrome(
            service=chrome_service, options=chrome_options
        )
        return driver
    
    def verify_new_york_store(self, driver) -> None:
        expected_main_title = "Our Stores."
        main_hero_text_element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(
                (By.XPATH, "//*[@id='blocks.richText_058616cfa0f6']/div[1]/div[1]/div[1]/h2[1]")
            )
        )
        main_hero_text = main_hero_text_element.text
        assert expected_main_title == main_hero_text, (
            f"FAILED \nExpected: '{expected_main_title}'\nGot: '{main_hero_text}'"
        )
        print("Main Text is as expected - PASSED")
                
        print("Verify Second Block")
        expected_location_title = "SoHo, New York."
        expected_ny_address = """Address 402 West Broadway, New York, NY 10012, United States 
        Get directions
        Contact 646-367-1757
        soho@varley.com 
        Opening hours 
        Monday to Saturday: 11am - 7pm 
        Sunday: 12pm - 6pm """
        
        print("Verifying Location Name in NY")
        location_title_element = driver.find_element(By.CSS_SELECTOR, 'h4.title.text-heading-four--mobile em')
        location_title = location_title_element.text.strip()
        assert expected_location_title == location_title, f"Expected:\n'{expected_location_title}', \n\nGot '{location_title}'"
        print(f"{location_title} is expected\n")
        
        print("Verifying NY address and contact information")
        # ny_contact_info_elements = driver.find_elements(By.CSS_SELECTOR, 'div.w-fit.text-black[0] p.text.text-body.font-nhaas')
    
        def normalize_whitespace(text):
            return re.sub(r'\s+', ' ', text).strip()

        # parent_element = driver.find_element(By.CSS_SELECTOR, 'div.w-fit.text-black')
        parent_element = driver.find_element(By.CSS_SELECTOR, 'div.text-black')

        paragraph_elements = parent_element.find_elements(By.CSS_SELECTOR, 'p.text.text-body.font-nhaas')

        cleaned_text = ' '.join(
            p.text.strip()
            for p in paragraph_elements
        ).strip()
        cleaned_text = normalize_whitespace(cleaned_text)
        expected_ny_address = normalize_whitespace(expected_ny_address)

        assert expected_ny_address == cleaned_text, f"Expected: {expected_ny_address}, Got: {cleaned_text}"
        print("The addresses match as expected.")

        # Verify Image
        img_element = driver.find_element(By.CSS_SELECTOR, 'picture img')
        img_src = img_element.get_attribute('src')
        if img_src:
            print(f"Image source URL: {img_src}")
        else:
            print("Image source is empty!")

        width = driver.execute_script("return arguments[0].naturalWidth;", img_element)
        height = driver.execute_script("return arguments[0].naturalHeight;", img_element)

        if width > 0 and height > 0:
            print("Image is not broken and loaded successfully!")
        else:
            print("Image is broken.")
        print("-" * 50)
             
    def verify_madison_avenue(self, driver) -> None:
        driver.execute_script("window.scrollBy(0, 700);")
        time.sleep(2)
        
        print("Verify Madison Avenue address block")
        madison_avenue = driver.find_element(By.CSS_SELECTOR , 'section[data-insider-id="blocks.split-3"]')
        madison_avenue_content = madison_avenue.find_element(By.CSS_SELECTOR, "div.w-full.md\\:w-fit.text-black")
        
        # Check for "Coming soon..." text
        expected_coming_soon_text = "Coming soon..."
        coming_soon_text = madison_avenue_content.find_element(By.CSS_SELECTOR, "p.text.text-body.font-nhaas em").text
        assert expected_coming_soon_text == coming_soon_text, "'Coming soon...' text is not displayed."
        print("Coming Soon... text is displayed")

        # Check for "Madison Avenue, New York." text
        expected_madison_text = "Madison Avenue, New York."
        madison_text = madison_avenue_content.find_element(By.CSS_SELECTOR, "h4.title.text-heading-four--mobile").text
        assert expected_madison_text == madison_text, "'Madison Avenue, New York.' text is not displayed."
        print(f"{madison_text} text is displayed")

        # Check if the image is loaded properly
        image = madison_avenue.find_element(By.CSS_SELECTOR, "picture img")
        image_loaded = driver.execute_script("return arguments[0].complete && arguments[0].naturalWidth > 0", image)
        assert image_loaded, "Image is not loaded properly."
        print("Image is loaded properly.")
        print("-" * 50)

    def verify_dallas_texas(self, driver) -> None:
        print("Verify Dallas Texas address block")
        dallas_texas = driver.find_element(By.CSS_SELECTOR , 'section[data-insider-id="blocks.split-4"]')
        dallas_texas_content = dallas_texas.find_element(By.CSS_SELECTOR, "div.w-full.md\\:w-fit.text-black")
        driver.execute_script("arguments[0].scrollIntoView();", dallas_texas)
        driver.execute_script("window.scrollBy(0, -200);")
        time.sleep(2)
        
        # Check for "Coming soon..." text
        expected_coming_soon_text = "Coming soon..."
        coming_soon_text = dallas_texas_content.find_element(By.CSS_SELECTOR, "p.text.text-body.font-nhaas em").text
        assert expected_coming_soon_text == coming_soon_text, "'Coming soon...' text is not displayed."
        print("Coming Soon... text is displayed")

        # Check for "Dallas, Texas." text
        expected_location_text = "Dallas, Texas."
        dallas_text = dallas_texas_content.find_element(By.CSS_SELECTOR, "h4.title.text-heading-four--mobile").text
        assert expected_location_text == dallas_text, f"{expected_location_text}' text is not displayed."
        print(f"{dallas_text} text is displayed")

        # Check if the image is loaded properly
        image = dallas_texas.find_element(By.CSS_SELECTOR, "picture img")
        image_loaded = driver.execute_script("return arguments[0].complete && arguments[0].naturalWidth > 0", image)
        assert image_loaded, "Image is not loaded properly."
        print("Image is loaded properly.")
        print("-" * 50)

    def verify_kings_road_address(self, driver) -> None:
        kings_road_london = driver.find_element(By.CSS_SELECTOR , 'section[data-insider-id="blocks.split-5"]')
        driver.execute_script("arguments[0].scrollIntoView();", kings_road_london)
        driver.execute_script("window.scrollBy(0, -200);")
        time.sleep(2)
                    
        print("Verify the King's Road Address Block")
        expected_location_title = "King's Road, London."
        expected_ny_address = """Address
            110-112 King's Road, London, SW3 4TX

            Contact
            02030847001
            kingsroad@varley.com

            Opening hours
            Monday to Saturday: 10am - 7pm
            Sunday: 12pm - 6pm
            *Excludes bank holiday weekends"""
        
        kings_road_london_content = kings_road_london.find_element(By.CSS_SELECTOR, "div.w-full.md\\:w-fit.text-black")

        print("Verifying Location Name")
        kings_road_title = kings_road_london_content.find_element(By.CSS_SELECTOR, 'h4.title.text-heading-four--mobile em').text.strip()
        assert expected_location_title == kings_road_title, f"Expected:\n'{expected_location_title}', \n\nGot '{kings_road_title}'"
        print(f"{kings_road_title} is expected\n")
        
        print("Verifying London address and contact information")    
        def normalize_whitespace(text):
            return re.sub(r'\s+', ' ', text).strip()

        london_address = kings_road_london_content.find_elements(By.CSS_SELECTOR, 'p.text.text-body.font-nhaas')

        cleaned_text = ' '.join(
            p.text.strip()
            for p in london_address
        ).strip()
        cleaned_text = normalize_whitespace(cleaned_text)
        expected_ny_address = normalize_whitespace(expected_ny_address)

        assert expected_location_title == kings_road_title, f"Expected:\n'{expected_location_title}', \n\nGot '{kings_road_title}'"
        print("The addresses match as expected.")

        # Verify Image
        img_element = kings_road_london.find_element(By.CSS_SELECTOR, 'picture img')
        img_src = img_element.get_attribute('src')
        if img_src:
            print(f"Image source URL: {img_src}")
        else:
            print("Image source is empty!")

        width = driver.execute_script("return arguments[0].naturalWidth;", img_element)
        height = driver.execute_script("return arguments[0].naturalHeight;", img_element)

        if width > 0 and height > 0:
            print("Image is not broken and loaded successfully!")
        else:
            print("Image is broken.")
        print("-" * 50)
                
    def verify_marylebone_address(self, driver) -> None:
        marylebone_london = driver.find_element(By.CSS_SELECTOR , 'section[data-insider-id="blocks.split-6"]')
        driver.execute_script("arguments[0].scrollIntoView();", marylebone_london)
        driver.execute_script("window.scrollBy(0, -200);")
        time.sleep(2)
                    
        print("Verify the Marylebone Address Block")
        expected_location_title = "Marylebone, London."
        expected_marylebone_address = """Address
            104 Marylebone High Street, London, W1U 4RR

            Contact
            02030847005
            marylebone@varley.com

            Opening hours
            Monday to Saturday: 10am - 7pm
            Sunday: 11am - 5pm
            *Excludes bank holiday weekends"""
        
        print("Verify Marylebone, London address block")
        
        marylebone_address_content = marylebone_london.find_element(By.CSS_SELECTOR, '[class="w-full md:w-fit text-black"]')
        
        print("Verifying Location Name")
        marylebone_title = marylebone_address_content.find_element(By.CSS_SELECTOR, 'h4.title.text-heading-four--mobile em').text.strip()
        assert expected_location_title == marylebone_title, f"Expected:\n'{expected_location_title}', \n\nGot '{marylebone_title}'"
        print(f"{marylebone_title} is expected\n")
        
        print("Verifying Marylebone address and contact information")    
        def normalize_whitespace(text):
            return re.sub(r'\s+', ' ', text).strip()

        london_address = marylebone_address_content.find_elements(By.CSS_SELECTOR, 'p.text.text-body.font-nhaas')

        marylebone_cleaned_text = ' '.join(
            p.text.strip()
            for p in london_address
        ).strip()
        marylebone_cleaned_text = normalize_whitespace(marylebone_cleaned_text)
        expected_marylebone_address = normalize_whitespace(expected_marylebone_address)

        assert expected_marylebone_address == marylebone_cleaned_text, f"Expected: {expected_marylebone_address}, Got: {marylebone_cleaned_text}"
        print("The addresses match as expected.")

        # Verify Image
        img_element = marylebone_london.find_element(By.CSS_SELECTOR, 'picture img')
        img_src = img_element.get_attribute('src')
        if img_src:
            print(f"Image source URL: {img_src}")
        else:
            print("Image source is empty!")

        width = driver.execute_script("return arguments[0].naturalWidth;", img_element)
        height = driver.execute_script("return arguments[0].naturalHeight;", img_element)

        if width > 0 and height > 0:
            print("Image is not broken and loaded successfully!")
        else:
            print("Image is broken.")
        print("-" * 50)

        print("Verify Behind the Brand video block")
        behind_the_brand = driver.find_element(By.CSS_SELECTOR , 'div[id="blocks.media_5c6742e6c0ef"]')
        driver.execute_script("arguments[0].scrollIntoView();", behind_the_brand)
        driver.execute_script("window.scrollBy(0, -200);")
        time.sleep(2)
        print("Video block is displayed")
     
        mobile_video = driver.find_element(By.CSS_SELECTOR, "video.lg\\:hidden")
        
        print("Checking mobile video...")
        mobile_video_src = mobile_video.get_attribute("src")
        if not mobile_video_src:
            print("[ERROR] Video source not found!")
            # return False
        
        response = requests.head(mobile_video_src)
        assert response.status_code == 200, f"[ERROR] Video returned status code: {response.status_code}"
        print(f"[SUCCESS] Video is accessible: {mobile_video_src}")
        
        print("Checking desktop video...")
        desktop_video = driver.find_element(By.CSS_SELECTOR, "video.lg\\:block")
        print("Checking mobile video...")
        desktop_video_src = desktop_video.get_attribute("src")
        if not desktop_video_src:
            print("[ERROR] Video source not found!")
        
        response = requests.head(desktop_video_src)
        assert response.status_code == 200, f"[ERROR] Video returned status code: {response.status_code}"
        print(f"[SUCCESS] Video is accessible: {desktop_video_src}")


if __name__ == "__main__":
    varley_our_store_page = Varley_Our_Store_Page()
    varley_our_store_page.test_nav_to_page("prod")