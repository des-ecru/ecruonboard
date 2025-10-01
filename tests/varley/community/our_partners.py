from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains

import time
import requests


class Varley_Our_Stockist:    
    def test_nav_to_page(self, env) -> None:
        driver = self.setup_driver()
        url = "https://www.varley.com/pages/our-partners"

        driver.get(url)
        time.sleep(2)
        self.verify_location_modal(driver)
        self.verify_that_the_page_is_viewable(driver)
        self.verify_the_content(driver)
  
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
    
    def verify_location_modal(self, driver):
        print("Verifying if Location modal appear")
        location_modal = driver.find_element(By.CSS_SELECTOR, "div[id^='headlessui-dialog-panel']")
        if location_modal.is_displayed():
            print("Location modal is displayed")
            
            cancel_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//button[contains(@class, 'uiButton') and contains(text(), 'Cancel')]"))
                )
            cancel_button.click()
            print("Clicking the Cancel button to close\n")
            time.sleep(2)
        else:
            print("Location modal is not displayed\n")
            
    # Test Case: C-140
    # Link: https://tuskr.live/project/1081dd66-4131-4537-a9e4-859653c572e7/test-case/05a61584-7b0b-4e1a-a814-c3356dc150cf
    def verify_that_the_page_is_viewable(self, driver):
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
    
    # Test Case: C-141,142
    # Link: https://tuskr.live/project/1081dd66-4131-4537-a9e4-859653c572e7/test-case/25a55d8e-e97f-48ef-a96b-fc1d898009fd
    def verify_the_content(self, driver):
        expected_h1 = "Found in over 1000 stores worldwide."
        partners_h1 = driver.find_element(By.CSS_SELECTOR, "h1.first\:mt-0")
        assert partners_h1.text == expected_h1, "Incorrect title text"
        print(f"Title text is correct: {expected_h1}")
        
        images = driver.find_elements(By.CSS_SELECTOR, ".md\:grid-cols-4 img")
        project_lists = [
            "NET-A-PORTER", "EQUINOX", "Neiman Marcus", "ANTHROPOLOGIE", "NORDSTROM", "shopbop",
            "SELFRIDGES & CO", "INTERMIX", "MYTHERESA", "bloomingdale's", "HOLT RENFREW", "EVEREVE",
            "REVOLVE", "goop", "HARVEY NICHOLS", "CARBON38", "FWRD", "Saks Fifth Avenue",
            "LUISAVIAROMA", "simons", "BERGDORF GOODMAN", "KaDeWe", "LE BON MARCHÉ", "PRINTEMPS"
        ]

        if len(images) != len(project_lists):
            print(f"Warning: Mismatch in project list ({len(project_lists)}) and image count ({len(images)})")

        print("Verify project list images")
        for project, img in zip(project_lists, images):
            if hasattr(img, "get_attribute"):
                src = img.get_attribute("src")
                response = requests.get(src)
                status_code = response.status_code
                assert status_code == 200, f"{project}: Status: {status_code}\n[FAIL]"
                print(f"Partner Name: {project} \nImage is not broken")
                initial_size = img.size
                actions = ActionChains(driver)
                actions.move_to_element(img).perform()
                time.sleep(2)

                after_hover_size = img.size

                if after_hover_size["width"] > initial_size["width"] and after_hover_size["height"] > initial_size["height"]:
                    print("Hover effect is Not working correctly.\n")
                else:
                    print("Hover effect is working.\n")
            else:
                print(f"[ERROR] {project}: Invalid image element detected")


if __name__ == "__main__":
    stockist_our_partners_page = Varley_Our_Stockist()
    stockist_our_partners_page.test_nav_to_page("prod")