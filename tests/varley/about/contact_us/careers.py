from selenium import webdriver
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome()

driver.get("https://www.varley.com/pages/careers")
driver.maximize_window()
time.sleep(3)

breadcrumb_link = driver.find_element(By.CSS_SELECTOR, ".capitalize:nth-child(1)")
breadcrumb_text = breadcrumb_link.text
breadcrumb_href = breadcrumb_link.get_attribute("href")

print("Verify if the breadcrumb contains 'Home'")
if breadcrumb_text.strip() == "Home":
    print("Breadcrumb contains 'Home'\n")
else:
    print("Breadcrumb does NOT contain 'Home'\n")

print("Verify if the link for Home is the expected URL")
expected_url = "https://www.varley.com/"
if breadcrumb_href == expected_url:
    print("Breadcrumb link matches expected URL")
else:
    print(f"Breadcrumb link does NOT match expected URL: Found {breadcrumb_href}")
    
expected_career_title = "Careers"
expected_career_text = (
    "We are always on the lookout for enthusiastic and talented people to join our team, share our vision and help create our future."
    "\n\nIf you’d like to join Varley, please email your CV to careers@varley.com"
)

career_title = driver.find_element(By.CSS_SELECTOR, ".first\:mt-0").text.strip()

assert career_title == expected_career_title, f"Title is not match!\nGot:{career_title} \n Expected:{expected_career_title}\n"
print("\nCareer Title matches the expected output.")

career_text_elements = driver.find_elements(By.CSS_SELECTOR, "div.mx-auto.max-w-\[680px\] div.portableText p")
career_text = "\n\n".join([" ".join(el.text.strip().splitlines()) for el in career_text_elements])
assert career_text == expected_career_text, f"Text is not match!\nGot:{career_text} \n Expected:{expected_career_text}\n"
print(f"\nText matches the expected output.\n{career_text}")

driver.quit()
