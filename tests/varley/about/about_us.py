from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager


import time

url = "https://www.varley.com/pages/about-varley"


class Varley_About_US_Page:
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
    # Test Case #:
    def verify_our_partner_page(self, driver):
        about_us_nav_links = driver.find_elements(By.CSS_SELECTOR, "section nav ul.flex.items-center > li")
        
        for link in about_us_nav_links:
            ActionChains(driver).move_to_element(link).perform()
            
            a_tag = link.find_element(By.CSS_SELECTOR, 'a')
            span_elements = a_tag.find_elements(By.CSS_SELECTOR, 'span')
            
            if span_elements and span_elements[0].text.strip():
                span_text = span_elements[0].text.strip()
            else:
                span_text = a_tag.text.strip()

            print(f"\nClicking the {span_text if span_text else '[No Text]'} link")
            link.click()
            time.sleep(2)
            
            if link.text == "Our Brand":
                our_brand_expected_h1_text = "Our brand."
                our_brand_expected_paragraph_text = (
                    "Founded in 2014 by husband-and-wife team Lara and Ben Mead, Varley is a contemporary fashion brand for the modern woman. "
                    "Our collections span the seasons, offering knitwear, outerwear, and everyday essentials, alongside activewear pieces to build a wardrobe for how you live and move.\n\n"
                    "Inspired by the women who wear Varley, we exist to instill quiet confidence, creating collections that enhance everything you already are.\n\n"
                    "As women’s lives evolve, so do we."
                )

                print("Validate if no broken image")
                image = driver.find_element(By.CSS_SELECTOR, "picture > img")
                img_src = image.get_attribute("src")
                if img_src and "http" in img_src:
                    print("Image src is valid")
                else:
                    print("Image src is invalid or missing:", img_src)

                print("Validate H1 text")
                our_brand_h1 = driver.find_element(By.CSS_SELECTOR, "div.text-white h1.title")
                h1_text = our_brand_h1.get_attribute("textContent").strip()
                assert h1_text == our_brand_expected_h1_text, f"Title text is incorrect. Found: {h1_text}"
                print(f"Title text is correct: {h1_text}")

                our_brand_expected_paragraph_text = (
                    "Founded in 2014 by husband-and-wife team Lara and Ben Mead, Varley is a contemporary fashion brand for the modern woman. "
                    "Our collections span the seasons, offering knitwear, outerwear, and everyday essentials, alongside activewear pieces to build a wardrobe for how you live and move.\n\n"
                    "Inspired by the women who wear Varley, we exist to instill quiet confidence, creating collections that enhance everything you already are.\n\n"
                    "As women’s lives evolve, so do we."
                )

                our_story_container = driver.find_element(By.CSS_SELECTOR, "div.w-full.md\\:w-fit.text-black > div")
                our_story_texts = our_story_container.find_elements(By.CSS_SELECTOR, "p, blockquote p")

                actual_paragraph_text = "\n\n".join([element.text.strip() for element in our_story_texts])
                
                assert actual_paragraph_text == our_brand_expected_paragraph_text, f"Paragraph text does not match.\n Got{actual_paragraph_text} \n Expected{our_brand_expected_paragraph_text}"
                print("Paragraph text matches expected content.\n")
                
                
            if link.text == "Our Story":
                
                years_expected_h1_text = "Our story."
                print("Validate Title text")
                our_story_section = driver.find_element(By.CSS_SELECTOR, "section[data-insider-id='blocks.split-3']")
                
                our_story_h1 = our_story_section.find_element(By.CSS_SELECTOR, "div.text-white h3.title")
                years_h1_text = our_story_h1.get_attribute("textContent").strip()
                assert years_h1_text == years_expected_h1_text, f"H1 text is incorrect.\nFound: {years_h1_text}\n Expected: {years_expected_h1_text}"
                print("H1 text is correct:", years_h1_text)
                
                our_story_expected_paragraph_text = (
                    '"Our idea was simple- combine the things we love and build a life around it."\n\n'
                    "Lara and Ben met in 2010 while training for the London Marathon. Their shared passions sparked an instant connection, and by 2014, Varley was born.\n\n"
                    "What started as a shared vision and merging of passions has grown into an international, family-run business with over 1,000 points of sale worldwide, and offices in London, Los Angeles, and New York.\n\n"
                    "Today, Varley is a close-knit team of thinkers, creators, and innovators, taking care of our clothes, each other, and our community."
                )

                our_story_container = our_story_section.find_element(By.CSS_SELECTOR, "div.w-full.md\\:w-fit.text-black > div")
                our_story_texts = our_story_container.find_elements(By.CSS_SELECTOR, "p, blockquote p")
                actual_paragraph_text = "\n\n".join([our_story_text.text.strip() for our_story_text in our_story_texts])
                if actual_paragraph_text == our_story_expected_paragraph_text:
                    print("Paragraph text matches expected content.")
                else:
                    print("Paragraph text does not match.")
                    
                print("Validate if no broken image")
                image = driver.find_element(By.CSS_SELECTOR, "picture > img")
                img_src = image.get_attribute("src")
                if img_src and "http" in img_src:
                    print("Image src is valid")
                else:
                    print("Image src is invalid or missing:", img_src)

            if link.text == "10 Years":
                years_expected_h1_text = "10 years of Varley."
                print("Validate Title text")
                years_section = driver.find_element(By.CSS_SELECTOR, "section[data-insider-id='blocks.split-4']")
                
                years_h1_text = years_section.find_element(By.CSS_SELECTOR, ".w-full > div > .text-heading-three--mobile")
                years_h1_text = years_h1_text.text.replace('\uFEFF', '').strip()
                years_expected_h1_text = years_expected_h1_text.replace('\uFEFF', '').strip()           

                assert years_h1_text == years_expected_h1_text, f"H1 text is incorrect.\nFound: {years_h1_text}\n Expected:{years_expected_h1_text}"
                print("Block Title is correct:", years_h1_text)
                
                years_expected_paragraph_text = (
                    "To mark Varley’s 10-year anniversary, co-founders Lara and Ben Mead sat down with Louise Roe at our new SoHo store. Together, they reflect on a decade of growth, challenges, and the journey that shaped Varley into what it is today.\n"
                    "Watch the full interview on WellSaid."
                )

                years_content_container = years_section.find_element(By.CSS_SELECTOR, ".py-\[120px\] > .w-full > div")
                years_content_texts = years_content_container.find_elements(By.CSS_SELECTOR, "p")

                paragraphs = [p.text.strip() for p in years_content_texts if p.text.strip()]

                # link_element = years_content_container.find_element(By.CSS_SELECTOR, "a")
                # link_text = link_element.text.strip()

                # if link_text and not paragraphs[-1].endswith(link_text):
                #     paragraphs[-1] += f" {link_text}"
     
                actual_years_paragraph_text = "\n".join(paragraphs)
                assert actual_years_paragraph_text == years_expected_paragraph_text, f"Paragraph text is incorrect.\nFound: {actual_years_paragraph_text}\n Expected: {years_expected_paragraph_text}"

                print("Paragraph text matches expected content.")
                
                print("Validate if no broken image")
                image = driver.find_element(By.CSS_SELECTOR, "picture > img")
                img_src = image.get_attribute("src")
                if img_src and "http" in img_src:
                    print("Image src is valid")
                else:
                    print("Image src is invalid or missing:", img_src)
            
            if link.text == "Our Stores":
                stores_expected_h1_text = "Our stores."
                print("Validate Title text")
                stores_section = driver.find_element(By.CSS_SELECTOR, "section[data-insider-id='blocks.split-5']")
                
                stores_title_text = stores_section.find_element(By.CSS_SELECTOR, "#blocks\.split_6ec4b0d7d50b .title").text
                assert stores_title_text == stores_expected_h1_text, f"H1 text is incorrect.\nFound: {stores_title_text}\n Expected:{stores_expected_h1_text}"
                print("Block Title is correct:", stores_title_text)
                
                stores_expected_paragraph_text = (
                    "Designed to reflect our brand values, our stores embody the same quality and quiet confidence as our clothing. Each space is crafted to elevate the everyday shopping experience, blending style and comfort for a welcoming feel.\n"
                    "Our flagship U.S. store, opened in October 2024, is located in the heart of SoHo, New York.\n"
                    "Visit our store page for more details."
                )

                stores_content_container = stores_section.find_element(By.CSS_SELECTOR, "#blocks\.split_6ec4b0d7d50b .flex > .flex > .w-full > div")
                stores_content_texts = stores_content_container.find_elements(By.CSS_SELECTOR, "p")

                paragraphs = [p.text.strip() for p in stores_content_texts if p.text.strip()]
     
                actual_stores_paragraph_text = "\n".join(paragraphs)
                assert actual_stores_paragraph_text == stores_expected_paragraph_text, f"Paragraph text is incorrect.\nFound: {actual_stores_paragraph_text}\n Expected: {stores_expected_paragraph_text}"
                print("Paragraph text matches expected content.")           
                
                print("Validate if no broken image")
                image = driver.find_element(By.CSS_SELECTOR, "picture > img")
                img_src = image.get_attribute("src")
                if img_src and "http" in img_src:
                    print("Image src is valid")
                else:
                    print("Image src is invalid or missing:", img_src)

            if link.text == "Our Partners":
                partners_expected_h1_text = "Found in over 1000 stores worldwide."
                print("Validate Title text")
                partners_section = driver.find_element(By.CSS_SELECTOR, "section[id='blocks.logoCloud_d8f167be7b41']")
                
                partners_title_text = partners_section.find_element(By.CSS_SELECTOR, ".max-w-\[750px\] > .title").text
                assert partners_title_text == partners_expected_h1_text, f"H1 text is incorrect.\nFound: {partners_title_text}\n Expected:{partners_expected_h1_text}"
                print("Block Title is correct:", partners_title_text)
                
                print("Validate if no broken image")
                partners_image = driver.find_element(By.CSS_SELECTOR, "picture > img")
                partners_img_src = partners_image.get_attribute("src")
                if partners_img_src and "http" in partners_img_src:
                    print("Image src is valid")
                else:
                    print("Image src is invalid or missing:", partners_img_src)
            
            if link.text == "Our People":
                people_expected_h1_text = "Our people."
                print("Validate Title text")
                people_section = driver.find_element(By.CSS_SELECTOR, "section[id='blocks.split_ec250562fc87']")
                
                people_title_text = people_section.find_element(By.CSS_SELECTOR, ".title").text
                assert people_title_text == people_expected_h1_text, f"H1 text is incorrect.\nFound: {people_title_text}\n Expected:{people_expected_h1_text}"
                print("Block Title is correct:", people_title_text)
                
                people_expected_paragraph_text = "What began as a company of two has evolved into a growing team of thinkers, creators, and innovators. Split across the UK and USA, our team is 90% female, embodying our identity as a brand by women, for women."

                people_content_container = people_section.find_element(By.CSS_SELECTOR, ".flex > .flex > .w-full > div > p").text
                assert people_content_container == people_expected_paragraph_text, f"Paragraph text is incorrect.\nFound: {people_content_container}\n Expected: {people_expected_paragraph_text}"
                print("Paragraph text matches expected content.")
                
                print("Validate if no broken image")
                image = driver.find_element(By.CSS_SELECTOR, "picture > img")
                img_src = image.get_attribute("src")
                if img_src and "http" in img_src:
                    print("Image src is valid")
                else:
                    print("Image src is invalid or missing:", img_src)
        
            if link.text == "Our Responsibility":
                responsibility_expected_h1_text = "Our responsibility."
                print("Validate Title text")
                responsibility_section = driver.find_element(By.CSS_SELECTOR, "section[id='blocks.split_34a3fe6a0981282cad755777106bbb10']")
                
                responsibility_title_text = responsibility_section.find_element(By.CSS_SELECTOR, ".title").text
                assert responsibility_title_text == responsibility_expected_h1_text, f"H1 text is incorrect.\nFound: {responsibility_title_text}\n Expected:{responsibility_expected_h1_text}"
                print("Block Title is correct:", responsibility_title_text)
                
                responsibility_expected_paragraph_text = (
                    "At Varley, responsibility is not a selling point. It is as fundamental as the fit of a garment.\n"
                    "Discover more on our responsibility page"
                )
                
                responsibility_content_texts = responsibility_section.find_element(By.CSS_SELECTOR, ".flex > .flex > .w-full > div")
                responsibility_content_text = responsibility_content_texts.find_elements(By.CSS_SELECTOR, "p")
                paragraphs = [p.text.strip() for p in responsibility_content_text if p.text.strip()]
                actual_responsibility_paragraph_text = "\n".join(paragraphs)
                assert actual_responsibility_paragraph_text == responsibility_expected_paragraph_text, f"Paragraph text is incorrect.\nFound: {actual_responsibility_paragraph_text}\n Expected: {responsibility_expected_paragraph_text}"
                print("Paragraph text matches expected content.")
                
                print("Validate if no broken image")
                image = driver.find_element(By.CSS_SELECTOR, "picture > img")
                img_src = image.get_attribute("src")
                if img_src and "http" in img_src:
                    print("Image src is valid")
                else:
                    print("Image src is invalid or missing:", img_src)


if __name__ == "__main__":
    our_partners = Varley_About_US_Page()
    our_partners.test_nav_to_page("prod")