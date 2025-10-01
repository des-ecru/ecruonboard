from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager

import time

url = "https://www.varley.com/pages/our-partners"


class Varley_Our_Partners_Page:
    # Link: https://tuskr.live/project/1081dd66-4131-4537-a9e4-859653c572e7/test-case/05a61584-7b0b-4e1a-a814-c3356dc150cf
    # Test Case#: C-140
    def test_nav_to_page(self, env) -> None:
        driver = self.setup_driver()
        driver.get(url)
        time.sleep(2)
        
        self.verify_our_partner_page(driver)
      
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
    
    # Links:
    # https://tuskr.live/project/1081dd66-4131-4537-a9e4-859653c572e7/test-case/25a55d8e-e97f-48ef-a96b-fc1d898009fd 
    # https://tuskr.live/project/1081dd66-4131-4537-a9e4-859653c572e7/test-case/c66cb404-f023-4086-9001-4f50b1bf5646
    # Test Case #: C-141 & C-142
    def verify_our_partner_page(self, driver):
        expected_output = "Found in over 1000 stores worldwide."
        
        print("Verifying the title")
        h1_element = driver.find_element(By.CSS_SELECTOR, "h1").text
        assert h1_element == expected_output, "Text is not the same"
        print(f"The {expected_output} is expected output. - PASSED\n")
        
        print("Verifying the hover and if the images are not broken")
        hover_divs = driver.find_elements(By.CSS_SELECTOR, "#our_partners .relative")

        company_names = [ 
            "NET-A-PORTER",
            "EQUINOX",
            "Neiman Marcus",
            "ANTHROPOLOGIE",
            "NORDSTROM",
            "shopbop",
            "SELFRIDGES & CO",
            "INTERMIX",
            "MYTHERESA",
            "bloomingdale's",
            "HOLT RENFREW",
            "EVEREVE",
            "REVOLVE",
            "goop",
            "Harvey Nichols",
            "CARBON38",
            "FWRD",
            "Saks Fifth Avenue",
            "LUISAVIAROMA",
            "simons",
            "BERGDORF GOODMAN",
            "KaDeWe",
            "LE BON MARCHÉ RIVE GAUCHE",
            "PRINTEMPS"
        ]
        
        print("Verifying the images if not broken and the hover is working")
        for index, div in enumerate(hover_divs):
            company_name = company_names[index] if index < len(company_names) else f"Company {index + 1}"
            
            img = div.find_element(By.TAG_NAME, "img")
            is_image_loaded = driver.execute_script(
                "return arguments[0].complete && arguments[0].naturalWidth > 0", img
            )
            print(f"{company_name} image is loaded: {'Yes' if is_image_loaded else 'No'}")
            
            actions = ActionChains(driver)
            actions.move_to_element(div).perform()
            driver.implicitly_wait(1)
            transform_property = driver.execute_script(
                "return window.getComputedStyle(arguments[0]).getPropertyValue('transform')", div
            )
            print(f"Hover animation for {company_name} is: {'Active' if transform_property != 'none' else 'None'}")


if __name__ == "__main__":
    our_partners = Varley_Our_Partners_Page()
    our_partners.test_nav_to_page("prod")