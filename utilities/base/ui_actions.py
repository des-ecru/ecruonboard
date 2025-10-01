import time
from typing import Literal, Optional

import selenium.webdriver.support.expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait

from utilities.drivers.driver_manager import Driver_Manager


class UI_Actions:

    # basic selector options by selenium
    selector_options = Literal[
        "css", "xpath", "id", "name", "class", "tag", "text", "partial_text"
    ]

    def _get_explicit_wait(
        self, timeout: int = Driver_Manager.timeout
    ) -> WebDriverWait:
        """get explicit wait, if timeout is not provided, use default timeout"""
        return (
            Driver_Manager.wait
            if timeout == Driver_Manager.timeout
            else WebDriverWait(Driver_Manager.driver, timeout)
        )

    def _get_selector_by(
        by: selector_options,
    ) -> By:
        """get selector by, default is css"""
        options: dict[str, By] = {
            "css": By.CSS_SELECTOR,
            "xpath": By.XPATH,
            "id": By.ID,
            "name": By.NAME,
            "class": By.CLASS_NAME,
            "tag": By.TAG_NAME,
            "text": By.LINK_TEXT,
            "partial_text": By.PARTIAL_LINK_TEXT,
        }
        return options[by]

    def find_elements(
        selector: str,
        by: selector_options = "css",
        timeout: int = Driver_Manager.timeout,
    ) -> list[WebElement]:
        """Find elements, return empty list if not found within timeout."""

        initial_timeout: int = Driver_Manager.timeout
        selector_type: By = UI_Actions._get_selector_by(by)
        found_elements: list[WebElement] = []

        if timeout != initial_timeout:
            try:
                Driver_Manager.set_implicit_wait(timeout)
                found_elements = Driver_Manager.driver.find_elements(
                    selector_type, selector
                )
            except Exception:
                found_elements = []
            finally:
                Driver_Manager.set_implicit_wait(initial_timeout)
        else:
            found_elements = Driver_Manager.driver.find_elements(
                selector_type, selector
            )
        return found_elements

    def find_element(
        selector: str,
        by: selector_options = "css",
        timeout: int = Driver_Manager.timeout,
        visible: bool = False,
        clickable: bool = False,
    ) -> WebElement:
        """find element, if not found raise exception, default timeout is 10 seconds.
        - visible = wait_for_element_visible if visible is True
        - clickable = wait_for_element_clickable if clickable is True
        """

        is_timeout_changed: bool = False
        initial_timeout: int = Driver_Manager.timeout
        selector_type: By = UI_Actions._get_selector_by(by)

        if timeout != initial_timeout:
            is_timeout_changed = True
            Driver_Manager.set_implicit_wait(timeout)
        element: WebElement = Driver_Manager.driver.find_element(
            selector_type, selector
        )
        if visible:
            UI_Actions.wait_for_element_visible(element, timeout)
        if clickable:
            UI_Actions.wait_for_element_clickable(element, timeout)
        if is_timeout_changed:
            Driver_Manager.set_implicit_wait(initial_timeout)
        return element

    def get_element_within(
        element: WebElement,
        selector: str,
        by: selector_options = "css",
        timeout: int = Driver_Manager.timeout,
    ) -> WebElement:
        """find element within element, if not found, raise exception"""
        found_element: WebElement | None = None
        selector_type: By = UI_Actions._get_selector_by(by)
        original_timeout: int = Driver_Manager.timeout

        if timeout != original_timeout:
            try:
                Driver_Manager.set_implicit_wait(timeout)
                found_element = element.find_element(selector_type, selector)
            except Exception:
                return None
            finally:
                Driver_Manager.set_implicit_wait(original_timeout)
        else:
            found_element = element.find_element(selector_type, selector)
        return found_element

    def get_elements_within(
        element: WebElement,
        selector: str,
        by: selector_options = "css",
        timeout: int = Driver_Manager.timeout,
    ) -> list[WebElement]:
        """Find elements within element, return empty list if not found within timeout."""
        selector_type: By = UI_Actions._get_selector_by(by)
        original_timeout: int = Driver_Manager.timeout
        found_elements: list[WebElement] = []

        if timeout != original_timeout:
            try:
                Driver_Manager.set_implicit_wait(timeout)
                found_elements = element.find_elements(selector_type, selector)
            except Exception:
                found_elements = []
            finally:
                Driver_Manager.set_implicit_wait(original_timeout)
        else:
            found_elements = element.find_elements(selector_type, selector)
        return found_elements

    def get_element(
        selector: str,
        by: selector_options = "css",
        timeout: int = Driver_Manager.timeout,
        visible: bool = False,
        clickable: bool = False,
    ) -> WebElement:
        """
        wait for element to be present, if not found, raise exception, default timeout is 10 seconds.
        - visible = wait_for_element_visible if visible is True
        - clickable = wait_for_element_clickable if clickable is True
        """
        wait = UI_Actions._get_explicit_wait(timeout)
        selector_type: By = UI_Actions._get_selector_by(by)
        element: WebElement = wait.until(
            EC.presence_of_element_located((selector_type, selector))
        )
        if visible:
            UI_Actions.wait_for_element_visible(element, timeout)
        if clickable:
            UI_Actions.wait_for_element_clickable(element, timeout)
        return element

    def get_elements(
        selector: str,
        by: selector_options = "css",
    ) -> list[WebElement]:
        """wait for all elements to be present, if not found raise exception"""
        selector_type: By = UI_Actions._get_selector_by(by)
        return Driver_Manager.wait.until(
            EC.presence_of_all_elements_located((selector_type, selector))
        )

    def wait_for_element_visible(
        element: WebElement, timeout: int = Driver_Manager.timeout, force: bool = False
    ) -> Optional[WebElement]:
        """
        wait for element to be visible, if not found, raise exception, default timeout is 10 seconds
        - force = force click using javascript
        """
        if force:
            is_visible = Driver_Manager.driver.execute_script(
                "return arguments[0] && arguments[0].offsetParent !== null;", element
            )
            return element if is_visible else None
        else:
            wait = UI_Actions._get_explicit_wait(timeout)
            return wait.until(EC.visibility_of(element))

    def get_element_text(
        element: WebElement, text: Optional[str] = None, timeout: int = 2
    ) -> str:
        """get element text, if text is provided, wait for element to have text equal to text"""

        element_text: str = element.text
        if not element_text:
            element_text = UI_Actions.get_element_attribute(element, "textContent")

        while_condition: bool = (not element_text) or (text and element_text != text)
        if while_condition:
            start_time: float = time.time()
            while time.time() - start_time < timeout:
                time.sleep(1)
                element_text: str = element.text
                if element_text == text or (element_text and not text):
                    return element_text
        return element_text

    def wait_for_element_invisible(
        element: WebElement | str,
        by: selector_options = "css",
        timeout: int = Driver_Manager.timeout,
        force: bool = False,
    ) -> bool:
        """wait for element to be invisible, if not found, raise exception"""
        driver = Driver_Manager.driver
        selector_type: By = UI_Actions._get_selector_by(by)

        if force:
            if isinstance(element, WebElement):
                return not driver.execute_script(
                    "return arguments[0] && arguments[0].offsetParent !== null;",
                    element,
                )
            else:
                try:
                    found = driver.find_element(selector_type, element)
                    return not driver.execute_script(
                        "return arguments[0] && arguments[0].offsetParent !== null;",
                        found,
                    )
                except Exception:
                    return True  # Element not found = considered invisible
        else:
            wait = UI_Actions._get_explicit_wait(timeout)
            if isinstance(element, WebElement):
                return wait.until(EC.invisibility_of_element(element))
            else:
                return wait.until(
                    EC.invisibility_of_element_located((selector_type, element))
                )

    def hover_element(element: WebElement) -> None:
        """hover over element, if not found, raise exception"""
        Driver_Manager.action.move_to_element(element).perform()
        Driver_Manager.wait.until(EC.visibility_of(element))

    def wait_for_element_clickable(
        element: WebElement, timeout: int = Driver_Manager.timeout, force: bool = False
    ) -> WebElement:
        """wait for element to be clickable, if not found, raise exception"""
        if force:
            is_clickable = Driver_Manager.driver.execute_script(
                "return arguments[0] && arguments[0].offsetParent !== null && !arguments[0].disabled;",
                element,
            )
            return element if is_clickable else None
        else:
            wait = UI_Actions._get_explicit_wait(timeout)
            return wait.until(EC.element_to_be_clickable(element))

    def wait_for_element_to_be_clickable(
        locator: str,
        by: selector_options = "css",
        timeout: int = Driver_Manager.timeout,
    ) -> WebElement:
        """wait for element to be clickable, if not found, raise exception"""
        element = UI_Actions.get_element(locator, by, timeout)
        Driver_Manager.wait.until(EC.element_to_be_clickable(element))
        return element

    def scroll_to_element(
        element: Optional[WebElement] = None, pixels_y: int = 0, pixels_x: int = 0
    ) -> None:
        """scroll to an element, if no element is provided (None) scroll by the amount of pixels"""
        action = Driver_Manager.action
        if (pixels_x or pixels_y) and not element:
            action.scroll_by_amount(pixels_x, pixels_y).perform()
        elif element and not pixels_x and not pixels_y:
            action.scroll_to_element(element).perform()
        elif element and (pixels_x or pixels_y):
            action.scroll_by_amount(pixels_x, pixels_y).perform()
            action.scroll_to_element(element).perform()
   
    def clear_text(element: WebElement, hard_clear: bool = False) -> None:
        """Clears text in an element."""
        element.clear()
        is_text: str = UI_Actions.get_element_text(element)
        if is_text and hard_clear:
            UI_Actions.hard_clear_text(element)

    def get_element_attribute(element: WebElement, attribute: str) -> str:
        """get element attribute, if not found, return empty string"""
        return element.get_attribute(attribute) or ""

    def get_element_css_property(element: WebElement, css_property: str) -> str:
        """get element value_of_css_property, if not found, return empty string"""
        return element.value_of_css_property(css_property) or ""

    
    def click_element(
        element: WebElement,
        force: bool = False,
        chain_click: bool = False,
        different_driver: WebDriver | None = None,
    ) -> None:
        """click an element, if force is True, force click using javascript,
        if chain_click is True, chain click using action chain,
        if different_driver is provided, use the different driver to click the element
        """
        if force or different_driver:
            # force click using javascript
            force_click_script: str = "arguments[0].click();"
            if different_driver:
                different_driver.execute_script(force_click_script, element)
            else:
                Driver_Manager.driver.execute_script(force_click_script, element)
        elif chain_click:
            # chain click using action chain
            Driver_Manager.action.click(element).perform()
        else:
            # normal click
            element.click()
