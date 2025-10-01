from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains

import time
driver = webdriver.Chrome()
driver.maximize_window()
driver.get("https://www.varley.com/")

ul_locator = (By.CSS_SELECTOR, "ul.hidden.lg\\:flex.order-1.w-full.flex-1.justify-center")
WebDriverWait(driver, 10).until(EC.presence_of_element_located(ul_locator))

print("\nVerifying GEOIP button")
wait = WebDriverWait(driver, 20)

button = driver.find_element((By.XPATH, "//button[@class='flex w-full items-center']"))
time.sleep(3)

if button.is_displayed():
    print("Button is properly displayed.")
    ActionChains(driver).move_to_element(button).perform()
    time.sleep(2)
else:
    print("Button is not displayed.")


button_text = button.text
expected_text = "Store: United States & Americas"
if expected_text in button_text:
    print("Button text is correct.")
else:
    print(f"Button text mismatch. Found: {button_text}")
    
driver.quit()