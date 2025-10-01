import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


driver = webdriver.Chrome()

# Navigating to the specified URL with the WebDriver
driver.get("https://www.varley.com/")
        
WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.headerGrid")))

# List of parent menu texts
expected_parent_menu_texts = [
    "New Arrivals" ,
    "Bestsellers", 
    "Shop All", 
    "Varley Live",
    "About"
]

expected_parent_menu_links = {
    "New Arrivals": "https://www.varley.com/collections/new-arrivals",
    "Bestsellers": "https://www.varley.com/collections/bestsellers",
    "Shop All": None,
    "Varley Live": "https://www.varley.com/pages/live-shopping",
    "About": "https://www.varley.com/pages/about-varley"
}

expected_parent_menu_texts = {
    "Shop All": {
        "Featured": { 
            "New Arrivals", "Bestsellers", "DoubleSoft®", "Club", 
            "The Outerwear Edit", "Varley Live"
        }, 
        "Clothing" : { 
            "Sweatshirts" , "Sweaters & Knitwear", "Tops", "Pants", "Sweatpants", 
            "Shorts", "Jumpsuits", "Dresses", "Swimwear" 
        },
        "Outerwear" : {
            "Jackets & Coats", "Quilted", "Gilets" , "Sherpa & Fleece" , "Puffers"
        },
        "Activewear" : {
            "Leggings", "Sports Bras", "Tops & Tanks" , "Midlayers & Jackets" , "Active Shorts",
            "Skorts" , "Club Dresses" 
        },
        "Accessories" : {
            "Bags" , "Hats & Caps" , "Footwear" , "Socks" , "Yoga Essentials" ,  "Scarves",
            "Gift Card"
        }
    }
}

expected_sub_menu_links = {
    "Featured" = "https://www.varley.com/collections/bestsellers",
    "New Arrivals" : {"https://www.varley.com/collections/new-arrivals", "Bestsellers", "DoubleSoft®", "Club", 
            "The Outerwear Edit", "Varley Live" },
    
        "Clothing" : { 
            "Sweatshirts" , "Sweaters & Knitwear", "Tops", "Pants", "Sweatpants", 
            "Shorts", "Jumpsuits", "Dresses", "Swimwear" 
        },
        "Outerwear" : {
            "Jackets & Coats", "Quilted", "Gilets" , "Sherpa & Fleece" , "Puffers"
        },
        "Activewear" : {
            "Leggings", "Sports Bras", "Tops & Tanks" , "Midlayers & Jackets" , "Active Shorts",
            "Skorts" , "Club Dresses" 
        },
        "Accessories" : {
            "Bags" , "Hats & Caps" , "Footwear" , "Socks" , "Yoga Essentials" ,  "Scarves",
            "Gift Card"
        }
}

# Expected submenu items for each parent menu
expected_submenus = {
    "New Arrivals": None,
    "Bestsellers": None,
    "Shop All":  ["Help Center", "Docs", "Team", "Careers"],
    "Varley Live": None,
    "About" : 
}



# Loop through each menu text
for menu_text in parent_menu_texts:
    # Find all parent menu elements
    parent_menus = WebDriverWait(driver, 20).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.n-header__item"))
    )

    # Locate the correct parent menu by text
    parent_menu = None
    for menu in parent_menus:
        if menu_text in menu.text.strip():
            parent_menu = menu
            break

    # If the parent menu was found, perform the hover action
    if parent_menu:
        hover = ActionChains(driver).move_to_element(parent_menu)
        hover.perform()
        time.sleep(2) 

        # Use WebDriverWait to wait for the first submenu item to be visible
        try:
            first_submenu_item = expected_submenus[menu_text][0]
            WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((By.XPATH, f"//div[@class='n-header__links']//a[contains(., '{first_submenu_item}')]"))
            )
            
        except Exception as e:
            print(f"Error while waiting for the first submenu item in '{menu_text}': {e}")
            continue

        # Find the submenu items under the parent menu
        submenu_items = parent_menu.find_elements(By.CSS_SELECTOR, "div.n-header__links a.n-header__link-element")

        # Extract the submenu text and compare it with expected values
        actual_submenu_texts = set()
        for item in submenu_items:
            try:
                text = item.find_element(By.CSS_SELECTOR, "div.n-heading--xxs").text.strip()
                link = item.get_attribute("href")
                actual_submenu_texts.add(text)
                
                # Check if the submenu item and link match the expected values
                if text in expected_submenus[menu_text] and expected_links.get(text) == link:
                    print(f"Submenu item '{text}' with link '{link}' is correct.")
                    
                else:
                    print(f"Submenu item '{text}' with link '{link}' does not match expected values.")
            except Exception as e:
                print(f"Submenu item could not be validated properly: {e}")

        # Compare the entire submenu list for this parent menu
        if actual_submenu_texts == set(expected_submenus[menu_text]):
            print(f"All submenu items for '{menu_text}' are correct. - PASSED\n")
        else:
            print(f"Submenu items for '{menu_text}' do not match expected values {expected_submenus[menu_text]} . Actual: {actual_submenu_texts}")
    else:
        print(f"Parent menu '{menu_text}' not found.")



# Function to verify submenu items
def verify_submenu(main_menu_name, submenu_items):
    try:
        # Locate and click the main menu item
        main_menu = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, f"//div[@id='header-{main_menu_name.lower()}']"))
        )
        main_menu.click()

        # Verify each submenu item
        for submenu_name, submenu_link in submenu_items.items():
            submenu_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, f"//a[@id='header-{submenu_name.lower().replace(' ', '-')}']"))
            )
            actual_link = submenu_element.get_attribute("href")
            if actual_link == submenu_link:
                print(f"Submenu item '{submenu_name}' with link '{submenu_link}' is correct.")
            else:
                print(f"Error in '{submenu_name}': Expected link '{submenu_link}', but found '{actual_link}'.")

        print(f"All submenu items for '{main_menu_name}' are correct. - PASSED\n")

    except Exception as e:
        print(f"Error while verifying submenu items in '{main_menu_name}': {e}")

# Define the submenu items for 'About'
about_submenu_items = {
    "Help Center": "https://www.hord.fi/help-center",
    "Docs": "https://docs.hord.fi/",
    "Team": "https://www.hord.fi/about",
    "Careers": "https://www.hord.fi/jobs"
}

# Verify the 'About' submenu
verify_submenu("About", about_submenu_items)


# "Launch App" button
launch_app_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, ".n-header__buttons .n-button"))
)
driver.execute_script("arguments[0].click();", launch_app_button)
print(f"Launch App button clicked and navigated- PASSED")

# Allow time for the new tab to open and load
if len(driver.window_handles) > 1:
    driver.switch_to.window(driver.window_handles[1])
    WebDriverWait(driver, 10).until(EC.url_contains("https://app.hord.fi/"))
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    
# "HyperYield" button
hyperyield_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, ".n-buttons-menu-wrapper .n-button"))
)
driver.execute_script("arguments[0].click();", launch_app_button)
print(f"HyperYield button clicked and navigated- PASSED")