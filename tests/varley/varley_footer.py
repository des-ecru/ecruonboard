from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
import requests

url = "https://www.varley.com/"

class Varley_Footer:    
    def test_nav_to_page(self, env) -> None:
        driver = self.setup_driver()
        url = "https://www.varley.com/"
        driver.get(url)
        time.sleep(2)
        
        self.verify_location_modal(driver)
        # self.test_verify_footer(driver)
        # self.verify_social_media_links(driver)
        # self.verify_geoip(driver)
        self.test_subscription(driver)
        self.test_footer_bar(driver)
      
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
            print("GeoIP modal is now hidden. Continuing with test")
        else:
            print("GeoIP modal is hidden. Continuing with test.")

    def test_verify_footer(self, driver) -> None:
        expected_footer_links = {
            "Help Centre": "/pages/help-centre",
            "Delivery & Returns": "/pages/delivery-and-returns",
            "Track My Order": "/pages/help-centre-tracking",
            "Size Guide": "/pages/help-centre-size-guide-new",
            "E-Gift Card": "/products/e-gift-card",
            "About Us": "/pages/about-varley",
            "Our Partners": "/pages/our-partners",
            "Journal": "/blogs/well-said",
            "Refer a Friend": "/pages/refer-a-friend",
            "Email & Live Chat": "/pages/contact-us",
            "Press": "/pages/press",
            "Wholesale": "/pages/wholesale",
            "Careers": "/pages/careers",
            "Our Stores": "/pages/our-stores",
        }
        print("FOOTER MENU NAVIGATION\n")
        
        footer_section = driver.find_element(By.CSS_SELECTOR, '[role="contentinfo"]')
        driver.execute_script("arguments[0].scrollIntoView();", footer_section)
        time.sleep(3)
        
        assert footer_section.is_displayed(), "Footer is not visible"
        print("Footer is displayed")

        footer_container = driver.find_element(By.CSS_SELECTOR, '.flex.w-full.flex-col.self-start')
        assert footer_container.is_displayed(), "Footer Container is not displayed"
        print("Footer Container is displayed")
        
        footer_links = driver.find_elements(By.CSS_SELECTOR, ".flex.flex-col.space-y-5 a")

        # Check each link
        all_correct = True
        for link in footer_links:
            text = link.text.strip()
            href = link.get_attribute("href")
            
            assert text in expected_footer_links, f"Unexpected link found: {text} - {href}"
            if expected_footer_links[text] not in href:  
                print(f"Mismatch: {text} | Expected: {expected_footer_links[text]} | Actual: {href}")
                all_correct = False
            print(f"Clicking the footer {text} link ")
            link.click()
            time.sleep(3)
            print("Verifying if url is correct")
            current_url = driver.current_url
            assert current_url == href , f"Url is not the same \nCurrent: {current_url}\n Expected: {href}"
            print("Footer link and page url is the same")
            driver.back()
            time.sleep(2)
            
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            footer_section = driver.find_element(By.CSS_SELECTOR, '[role="contentinfo"]')
            driver.execute_script("arguments[0].scrollIntoView();", footer_section)
            footer_container = driver.find_element(By.CSS_SELECTOR, '.flex.w-full.flex-col.self-start')
            footer_links = driver.find_elements(By.CSS_SELECTOR, ".flex.flex-col.space-y-5 a")
            
            # print(f"{text} : {href}\n")

        if all_correct:
            print("All footer links match the expected output!")
     
    def verify_social_media_links(self, driver):
        social_media_links = {
            "facebook": "https://www.facebook.com/varleyofficial/",
            "insta": "https://www.instagram.com/varley/",
            "pinterest": "https://uk.pinterest.com/varleyofficial/"
        }
        
        print("\nFOOTER MENU > Social Media Block and Logo \n")
        social_media_container = driver.find_element(By.CSS_SELECTOR, '[class*="sm:flex"]')
        driver.execute_script("arguments[0].scrollIntoView();", social_media_container)
        time.sleep(3)
        assert social_media_container.is_displayed(), "Social Media container is not displayed"
        print("Social Media container is displayed")
        social_media_list = social_media_container.find_element(By.CSS_SELECTOR, 'ul[class*="lg:flex"]')
        social_links = social_media_list.find_elements(By.CSS_SELECTOR, "li > a[href]")
        original_window = driver.current_window_handle
        for link in social_links:
            href = link.get_attribute('href')
            
            if href:
                svg = link.find_element(By.TAG_NAME, 'svg')
                if svg.is_displayed():
                    print(f"SVG found and displayed for link: {href}")
                else:
                    print(f"SVG found but not displayed for link: {href}")

                link.click()
                time.sleep(5)
                
                new_window = [window for window in driver.window_handles if window != original_window][0]
                driver.switch_to.window(new_window)
                time.sleep(3)
                
                current_url = driver.current_url
                print(f"Opened new tab with URL: {current_url}")
                
                matched = any(current_url == url for url in social_media_links.values())
                assert matched, f"Unexpected URL: {current_url}"
                print("Url is matched \n Going back to Home Page")
                driver.close()
                driver.switch_to.window(original_window)

            print("\nVerifying VARLEY Logo")
            varley_logo_footer = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "div.hidden.lg\\:block svg"))
            )
            svg_inner_html = varley_logo_footer.get_attribute('innerHTML').strip()

            if svg_inner_html:
                print("SVG contains elements and is not empty.")
            else:
                print("SVG is empty.\n")
    
    def verify_geoip(self, driver) -> None:
        expected_href = {
            "United Kingdom": "https://uk.varley.com/",
            "United States & Americas": "https://www.varley.com/",
            "European Union": "https://eu.varley.com/",
            "Rest of the world": "https://uk.varley.com/"
        }
        print("\nVerifying GEOIP button")
        geoip_button = driver.find_element(By.CSS_SELECTOR, '.order-none:nth-child(3) > .flex')
        driver.execute_script("arguments[0].scrollIntoView();", geoip_button)
        time.sleep(3)
        assert geoip_button.is_displayed(), "GeoIP Button is not displayed."
        print("Geoip Button is properly displayed.")
        
        print("Clicking the GEOIP button")
        geoip_button.click()
        time.sleep(3)
        geoip_modal = driver.find_element(By.CSS_SELECTOR, 'div[id^="headlessui-dialog-panel"]')

        assert geoip_modal.is_displayed(), "GeoIP Modal is not displayed."
        print("Geoip Modal is displayed.")
        
        print("Verifying US, EU, UK and ROW locations")
        location_container = geoip_modal.find_element(By.CSS_SELECTOR, '[class*="px-15"]')
        locations = location_container.find_elements(By.CSS_SELECTOR, 'button[class*="focus-outline"]')

        for i in range(len(locations)):
            # Re-locate buttons fresh every iteration (because DOM might reload)
            location_container = geoip_modal.find_element(By.CSS_SELECTOR, 'div.px-15')
            locations = location_container.find_elements(By.CSS_SELECTOR, 'button.focus-outline')
            location = locations[i]

            spans = location.find_elements(By.TAG_NAME, 'span')
            assert len(spans) >= 2, "Could not find expected span elements in location button"
            country = spans[0].text.strip()
            currency = spans[1].text.strip()
            print(f"{country} : {currency}")

            img = location.find_element(By.CSS_SELECTOR, 'img.mr-5')
            img_src = img.get_attribute("src")
            response = requests.get(img_src)
            assert response.status_code == 200, f"Location Flag for {country} is broken"
            print(f"Location Flag for {country} is NOT broken and visible")
            location.click()
            time.sleep(5)

            current_url = driver.current_url
            expected_url = expected_href.get(country)
            assert expected_url is not None, f"No expected URL configured for {country}"
            assert current_url.startswith(expected_url), (
                f"URL mismatch for {country}.\nExpected: {expected_url}\nGot: {current_url}"
            )

            print(f"{country} URL is correct: {current_url}")
            print("Going back to previous page")
            driver.back()
            time.sleep(3)
            geoip_button = driver.find_element(By.CSS_SELECTOR, '.order-none:nth-child(3) > .flex')
            print("Reopening the geoip modal")
            driver.execute_script("arguments[0].scrollIntoView();", geoip_button)
            time.sleep(3)
            assert geoip_button.is_displayed(), "GeoIP Button is not displayed."
            print("Geoip Button is properly displayed.")
            
            print("Clicking the GEOIP button")
            geoip_button.click()
            time.sleep(3)
            geoip_modal = driver.find_element(By.CSS_SELECTOR, 'div[id^="headlessui-dialog-panel"]')
            assert geoip_modal.is_displayed(), "GeoIP Modal is not displayed."
            print("Geoip Modal is displayed.")

    def test_subscription(self, driver) -> None:
        expected_text = "Subscribe to our newsletter & receive 10% off your first order"
        print("\nVerify the Subscription block")
        subscription_container = driver.find_element(By.CSS_SELECTOR, '[class*="lg:w-[264px]"]')
        driver.execute_script("arguments[0].scrollIntoView();", subscription_container)
        time.sleep(3)
        assert subscription_container.is_displayed(), "Subscription block is not displayed."
        print("Subscription block is properly displayed.")
    
        h4_text = driver.find_element(By.CSS_SELECTOR, '[class*="mb-2"]')
        title_text = h4_text.text
        assert title_text == expected_text, "Title text is incorrect"
        print("Title text is correct")
        
        subscriber_address = "lourdes@ecrubox.com"
        email_address = driver.find_element(By.CSS_SELECTOR, 'input[placeholder="Email address"]') 
        email_address.send_keys(subscriber_address)
        print(f"Subscriber's Email: {subscriber_address}")
        time.sleep(3)
        
        send_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[aria-label="Sign up"]'))
            )
        send_btn.click()
        time.sleep(3)
        print("Clicked the Enter button")
        
        thank_you_text1 = driver.find_element(By.CSS_SELECTOR, '[class^="mb-1 text-sm"]').text
        
        thank_you_text2 = driver.find_element(By.CSS_SELECTOR, '[class^="mb-3 text-sm"]').text
        expected_thank1 = "Thanks for subscribing!"
        expected_thank2 = "Enjoy 10% off with this code at checkout:"
        
        assert thank_you_text1 == expected_thank1, f" '{expected_thank1}' is incorrect"
        assert thank_you_text2 == expected_thank2, f" '{expected_thank2}' is incorrect"
        print(f"{expected_thank1}\n{expected_thank2}")
        
        code = driver.find_element(By.CSS_SELECTOR, '[class^="mb-10 flex"] [class^="font-medium"] ')
        hello_varley = code.text
        expected_code = "HELLOVARLEY"
        assert hello_varley == expected_code , f"'{expected_code}' is not displayed"
        print(f"{expected_code} is displayed")
        
    def test_footer_bar(self, driver) -> None:
        expected_footer_bar_links = {
            "T&C's": "https://www.varley.com/pages/terms-and-conditions",
            "Privacy Policy": "https://www.varley.com/pages/privacy-policy",
            "Cookie Policy": "https://www.varley.com/pages/cookie-policy",
            "Accessibility Statement": "https://www.varley.com/pages/accessibility-statement"
        }
        
        print("\nVerify the Footer bar")
        footer_bar = driver.find_element(By.CSS_SELECTOR, '[class*="content-between"]')
        driver.execute_script("arguments[0].scrollIntoView();", footer_bar)
        time.sleep(3)
        assert footer_bar.is_displayed(), "Footer bar is not displayed."
        print("Footer bar is properly displayed.")
        
        print("\nVerify the Footer Bar links")
        footer_links = driver.find_elements(By.CSS_SELECTOR, "div[class*='mt-5'] ul li a")

        for i in range(len(footer_links)):
            
            footer_links = driver.find_elements(By.CSS_SELECTOR, "div[class*='mt-5'] ul li a")
            link = footer_links[i]
            text = link.text.strip()
            
            if text == "|": 
                continue
            expected_url = expected_footer_bar_links.get(text)
            print(f"Clicking the {text} link")
            link.click()
            time.sleep(3)
            current_url = driver.current_url
            assert current_url == expected_url, f"URL mismatch for {text}."
            print("URL verified. \n Navigating back to Home Page")
            
            driver.back()
            time.sleep(2)
            footer_links = driver.find_elements(By.CSS_SELECTOR, "div[class*='mt-5'] ul li a")

        print("\nVerify footbar middle text")
        if_you_are_using_container = driver.find_element(By.CSS_SELECTOR, "div.portableText.font-light.text-\\[12px\\].sm\\:text-sm.md\\:text-xs")
        assert if_you_are_using_container.is_displayed()
        
        p_element = if_you_are_using_container.find_element(By.CSS_SELECTOR, "p.relative.first-of-type\\:mt-0.font-light.text-\\[12px\\].sm\\:text-sm.md\\:text-xs")
        span_element = p_element.find_element(By.CSS_SELECTOR, "span")
        assert "If you are using a screen reader and are having problems using this website, please email us at" in span_element.text

        link_element = p_element.find_element(By.CSS_SELECTOR, "a.underline.transition-opacity.duration-200.hover\\:opacity-60")
        assert link_element.text == "support@varley.com"
        assert link_element.get_attribute("href") == "mailto:support@varley.com"
        print("Middle text verified\n")
        
        print("Verify Accessibility and Trademark content")
        accessibility_div = driver.find_element(By.CSS_SELECTOR, "div.order-2.flex.flex-col.font-light.text-\\[12px\\].sm\\:text-sm.md\\:text-xs.mt-5.md\\:mt-8.lg\\:mt-0")
        
        accessibility = driver.find_element(By.CSS_SELECTOR, "div.hidden.lg\\:block #footerAccessibly")
        assert accessibility.is_displayed()
        print("Accessibility section is displayed")

        expected_access_text = "Accessibility"
        accessibility_text = accessibility.find_element(By.CSS_SELECTOR, "span.text-\\[12px\\].font-light.sm\\:text-sm")
        assert accessibility_text.text == expected_access_text, "Incorrect 'Accessibility' text"
        print(f"{expected_access_text} is displayed")

        copyright_div = accessibility_div.find_element(By.CSS_SELECTOR, "div.text-center.text-\\[9px\\].md\\:whitespace-nowrap.md\\:text-right.md\\:text-\\[12px\\]")
        assert "2025 Varley International Holdings Limited. All rights reserved" in copyright_div.text
        print("'2025 Varley International Holdings Limited. All rights reserved' is displayed")
                
                

if __name__ == "__main__":
    varley_footer = Varley_Footer()
    varley_footer.test_nav_to_page("prod")

