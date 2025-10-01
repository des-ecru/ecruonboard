from selenium import webdriver
from selenium.webdriver.common.by import By

import time
import requests
import re

driver = webdriver.Chrome()

# Navigate to the specified URL
driver.get("https://www.varley.com/pages/responsibility")
driver.maximize_window()
time.sleep(3)

li_elements = driver.find_elements(By.CSS_SELECTOR, 'section nav ul.flex.items-center.justify-center.space-x-20 li')

for li in li_elements:
    a_tag = li.find_element(By.CSS_SELECTOR, 'a')

    href_value = a_tag.get_attribute('href')
    span_elements = a_tag.find_elements(By.CSS_SELECTOR, 'span')
    
    if span_elements and span_elements[0].text.strip():
        span_text = span_elements[0].text.strip()
    else:
        span_text = a_tag.text.strip()

    print(f"\nClicking the {span_text if span_text else '[No Text]'} link")
    li.click()
    time.sleep(2)

    # Verify Responsibility section
    if span_text == "responsibility":
        # Verify Responsibility section Text
        text_element = driver.find_element(By.CSS_SELECTOR, "h4.title.font-plantin")
        expected_text = "For us, responsibility is not a selling point. It is as fundamental as the fit of a garment."

        if text_element.text.strip() == expected_text:
            print("Text matches the expected value.")
        else:
            print(f"Text mismatch! Found: {text_element.text.strip()}")

        # Verify Responsibility section Image
        image_element = driver.find_element(By.CSS_SELECTOR, "picture[data-insider-id='blocks.heroBanner-2-image'] img")
        image_url = image_element.get_attribute("src")

        if image_url:
            response = requests.get(image_url)
            if response.status_code == 200:
                print("Image is not broken.")
            else:
                print(f"Image is broken. Status code: {response.status_code}")
        else:
            print("No image found.")
        
        # Second Block
        expected_responsibility_text = {
            "Committed to quality.": "We’re committed to making versatile clothes that live on, season after season. Prioritizing quality and longevity, we design items in colors and styles that remain timeless in your wardrobe, allowing you to make the responsible choice to buy less and buy better.",
            "Considered materials.": "We use responsibly sourced, recycled, and certified materials wherever possible. Our premium puffer coats feature either 100% responsibly sourced down or 100% recycled polyester insulation and we are transitioning to 100% BCI (Better Cotton Initiative) cotton for our core knitwear.",
            "Conscious production.": "We prioritize safe working conditions for our product makers, ensuring our suppliers meet global standards for working conditions and wages. Our Move and Always fabrics are bluesign® APPROVED, featuring eco-friendly dyeing and printing methods in these collections.",
            "Environmentally aware.": "We believe in only making what we need by cutting our collections to order, minimizing our waste output. We use recycled polythene to pack our garments and we’ve also eliminated single-use plastics from our e-commerce packaging, utilizing recycled and FSC Certified materials instead."
        }

        print("Scrolling to second block of Responsibility section")
        sections = driver.find_element(By.CSS_SELECTOR, 'section[id="blocks.contentColumns_45b8dbfa195a"]')
        driver.execute_script("arguments[0].scrollIntoView();", sections)
        driver.execute_script("window.scrollBy(0, -200);")

        # Get the sub-sections inside the Responsibility block
        section_list = sections.find_elements(By.CSS_SELECTOR, 'div[id="columns"] > div[class^=" border-b-2"]')

        for section in section_list:            
            title_element = section.find_element(By.CSS_SELECTOR, 'h3.title')
            body_element = section.find_element(By.CSS_SELECTOR, 'p.text.text-body.font-nhaas')
            title_text = title_element.text.replace("\n", " ").strip()

            expected_body = expected_responsibility_text.get(title_text)  # Make sure to use the correct dictionary

            if expected_body:
                if body_element.text.strip() == expected_body:
                    print(f"Section '{title_text}' content is correct!")
                else:
                    print(f"Section '{title_text}' content is incorrect. \n --> {body_element.text.strip()} ")
            else:
                print(f"Title '{title_text}' not found in expected text.")

        # Verify Second Block Image
        image_element = driver.find_element(By.CSS_SELECTOR, "picture[data-insider-id='blocks.heroBanner-2-image'] img")
        image_url = image_element.get_attribute("src")

        if image_url:
            response = requests.get(image_url)
            if response.status_code == 200:
                print("Image is not broken.")
            else:
                print(f"Image is broken. Status code: {response.status_code}")
        else:
            print("No image found.")
        
    # Verify Fairly Made® section
    if "Made®" in span_text:
        print("Verify Fairly Made section content")
        fairly_made_section = driver.find_element(By.CSS_SELECTOR, 'section[id="blocks.splitQuote_cef2657f0c90"]')
        driver.execute_script("arguments[0].scrollIntoView();", fairly_made_section)
        driver.execute_script("window.scrollBy(0, -200);")
        
        fairly_made_content1 = fairly_made_section.find_element(By.CSS_SELECTOR, 'h4.title')
        title_text = title_element.text.replace("\n", " ").strip()
        expected_fairly_made_content1 = "Our responsibility starts with transparency. Understanding and sharing the traceability of our products enables us to improve our social and environmental impact."
        
        assert fairly_made_content1.text == expected_fairly_made_content1, "Fairly Made Content title is not correct"
        print("Title is correct")
        
        print("Verify the Fairly made image")
        fairly_made_image = driver.find_element(By.CSS_SELECTOR, '.items-center > picture > .h-full')
        img_src = fairly_made_image.get_attribute("src")
        response = requests.get(img_src)
        assert response.status_code== 200, "Image is Broken."
        print("-Image is not broken ")
        
        print("Verify the main content")
        fairly_title = driver.find_element(By.CSS_SELECTOR, ".px-6 .title")
        driver.execute_script("arguments[0].scrollIntoView();", fairly_title)
        driver.execute_script("window.scrollBy(0, -200);")
        expected_fairly_title = "Fairly Made®."
        assert fairly_title.text == expected_fairly_title, "Fairly Made title is not correct"
        print("Title is correct")
        
        fairly_paragraph = driver.find_elements(By.CSS_SELECTOR, "div.mt-5.lg\:mt-6 p")
        expected_fairly_paragraph = (
            "In line with our commitment to responsibility, we've partnered with Fairly Made®. "
            "This collaboration gives us the tools to measure the impact of our actions and enhance transparency in tracing our product origins. "
            "From February 2024, Fairly Made will begin a project to measure and score our products’ environmental and social impact. "
            "This ongoing initiative allows us to understand the traceability of our products and work towards a more transparent and responsible future."
        )        
        
        actual_fairly_paragraph = " ".join(" ".join([p.text for p in fairly_paragraph if p.text.strip()]).split())

        assert actual_fairly_paragraph == expected_fairly_paragraph, f"Fairly Made Content is not correct \nGot:{actual_fairly_paragraph} \nExpected: {expected_fairly_paragraph}"
        print("Content is correct")
        
        print("Verify the Video")
        fairly_made_video = driver.find_element(By.CSS_SELECTOR, '.\!pointer-events-auto:nth-child(2)')
        driver.execute_script("arguments[0].scrollIntoView();", fairly_made_video)
        driver.execute_script("window.scrollBy(0, -200);")
        
        ready_state = driver.execute_script("return arguments[0].readyState;", fairly_made_video)
        if ready_state >= 2:  # 2 = HAVE_CURRENT_DATA, meaning the video has loaded enough to play
            print("Video is loading properly.")
        else:
            print("Video might be broken or not loading correctly.")
        

    # Verify Packaging section
    if "Packaging" in span_text:
        print("Scrolling to Packaging section")
        fairly_made_section = driver.find_element(By.CSS_SELECTOR, 'section[id="blocks.splitQuote_cef2657f0c90"]')
        driver.execute_script("arguments[0].scrollIntoView();", fairly_made_section)
        driver.execute_script("window.scrollBy(0, -200);")

        print("Verify the Packaging image")
        packaging_image = driver.find_element(By.CSS_SELECTOR, '.order-1:nth-child(1) .h-full')
        img_src = packaging_image.get_attribute("src")
        response = requests.get(img_src)
        assert response.status_code == 200, "Image is Broken."
        print("Image is not broken ")
        
        print("Verify the Packaging content")
        packaging_title = driver.find_element(By.CSS_SELECTOR, ".flex:nth-child(2) > .w-full > div > .title")
        driver.execute_script("arguments[0].scrollIntoView();", packaging_title)
        driver.execute_script("window.scrollBy(0, -200);")
        expected_packaging_title = "Packaging."
        assert packaging_title.text == expected_packaging_title, f"Packaging title is not correct \nGot{packaging_title.text} \nExpected:{expected_packaging_title}"
        print("Title is correct")
        
        packaging_paragraph = driver.find_elements(By.CSS_SELECTOR, ".lg\:h-full:nth-child(2) div:nth-child(2) p")
        expected_packaging_paragraph = (
            "We prioritise responsible packaging by using recycled polythene and eliminating single-use plastics from our e-commerce operations. "
            "Hang tags are FSC Certified, supporting responsible forestry, and poly bags are made from 100% recycled plastic. "
            "Our UK, EU and US packaging is FSC Certified and recyclable. From 2024, all our care labels and internal woven labels will be made from recycled polyester."
        )
     
        actual_fairly_paragraph = " ".join(p.text.strip() for p in packaging_paragraph if p.text.strip())

        # Normalize whitespace
        normalized_expected = " ".join(expected_packaging_paragraph.split())
        normalized_actual = " ".join(actual_fairly_paragraph.split())

        assert normalized_actual == normalized_expected, f"Packaging Paragraph is not correct \nGot:{normalized_actual} \nExpected: {normalized_expected}"

        print("Content is correct")

        
    # Verify Partners section
    if "partners" in span_text:
        print("Scrolling to Smart Works section")
        smartworks_section = driver.find_element(By.CSS_SELECTOR, 'section[id="blocks.split_67e4bb872c52"]')
        driver.execute_script("arguments[0].scrollIntoView();", smartworks_section)
        driver.execute_script("window.scrollBy(0, -200);")

        print("Verify the Smart Works image")
        smartworks_image = driver.find_element(By.CSS_SELECTOR, '.order-1:nth-child(2) .h-full')
        img_src = smartworks_image.get_attribute("src")
        response = requests.get(img_src)
        assert response.status_code == 200, "Smart Works is Broken."
        print("Smart Works is not broken ")
        
        print("Verify the Smart Works content")
        smartworks_title = driver.find_element(By.CSS_SELECTOR, ".flex:nth-child(1) > .w-full .title")
        driver.execute_script("arguments[0].scrollIntoView();", smartworks_title)
        driver.execute_script("window.scrollBy(0, -200);")
        expected_smartworks_title = "Smart Works."
        assert smartworks_title.text == expected_smartworks_title, f"Smart Works title is not correct \nGot{smartworks_title.text} \nExpected:{expected_smartworks_title}"
        print("Title is correct")
        
        smartworks_paragraph = driver.find_elements(By.CSS_SELECTOR, ".lg\:h-full:nth-child(1) div:nth-child(2) p")
        expected_smartworks_paragraph = (
            "We are proud to partner with Smart Works, a UK charity that helps women secure employment and change the trajectory of their lives."
            "As a registered partner, Varley donates clothes to Smart Works on a rolling basis, supporting the charity's work to help more women across the UK through the power of clothing." 
            "This partnership not only limits waste but also helps to provide women with the quiet confidence to live life on their own terms. "
            "Read more on WellSaid"
        )        
        
        actual_smartworks_paragraph = " ".join([p.text.strip() for p in smartworks_paragraph if p.text.strip()])
        
        normalized_actual = re.sub(r'\.\s*', '. ', actual_smartworks_paragraph)  # Ensure space after every period
        normalized_actual = " ".join(normalized_actual.split())  # Remove extra spaces and newlines

        normalized_expected = re.sub(r'\.\s*', '. ', expected_smartworks_paragraph)  # Ensure space after every period
        normalized_expected = " ".join(normalized_expected.split())  # Remove extra spaces and newlines

        assert normalized_actual == normalized_expected, f"Smart Works Content is not correct \nGot:{normalized_actual} \nExpected: {normalized_expected}"


        print("Content is correct")
        
        
        


    driver.execute_script("window.scrollTo(0, 0);")
    time.sleep(1)


driver.quit()