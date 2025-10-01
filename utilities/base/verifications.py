from datetime import datetime
from typing import Literal, Optional

import allure
from selenium.webdriver.remote.webelement import WebElement

from utilities.base.ui_actions import UI_Actions


class Verifications:
    @allure.step("Verify element displayed")
    def verify_element_displayed(element: WebElement) -> None:
        assert element.is_displayed() is True

    @allure.step("Verify element NOT displayed")
    def verify_element_not_displayed(element: WebElement) -> None:
        assert element.is_displayed() is False

    @allure.step("Verify text includes")
    def verify_text_includes(
        text: str, words: list[str], message: str = ""
    ) -> None:
        for word in words:
            assert (
                word.lower() in text.lower()
            ), f"{message}. Actual: {text}, Expected includes: {word}"

    @allure.step("Verify text not includes")
    def verify_text_not_includes(
        text: str, words: list[str], message: str = ""
    ) -> None:
        for word in words:
            assert (
                word.lower() not in text.lower()
            ), f"{message}. Actual: {text}, Expected not includes: {word}"

    @allure.step("Verify element text")
    def verify_element_text(
        element: WebElement,
        text: str,
        condition: Optional[Literal["equals-upper", "equals-lower"]] = None,
        message: str = "",
    ) -> None:
        """verify element text is equal to text with optional case insensitive comparison"""
        element_text: str = UI_Actions.get_element_text(element)
        if condition == "equals-upper":
            text: str = text.upper()
            element_text: str = element_text.upper()
        elif condition == "equals-lower":
            text: str = text.lower()
            element_text: str = element_text.lower()
        assert (
            element_text == text
        ), f"{message}. Actual: {element_text}, Expected: {text}"

    @allure.step("Verify object is None")
    def verify_object_is_None(obj: object) -> None:
        assert obj is None

    @allure.step("Verify object is not None")
    def verify_object_is_not_None(obj: object) -> None:
        assert obj is not None

    @allure.step("Verify element invisible")
    def verify_element_invisible(element: WebElement) -> None:
        assert UI_Actions.wait_for_element_invisible(element) is True

    @allure.step("Verify element visible")
    def verify_element_visible(element: WebElement) -> None:
        assert UI_Actions.wait_for_element_visible(element) is True

    @allure.step("Verify equals")
    def verify_equals(
        actual: object, expected: object, message: str = ""
    ) -> None:
        assert actual == expected, (
            f"{message}. Actual: {actual}, Expected: {expected}"
        )
    
    @allure.step("Verify lists equal")
    def verify_lists_equal(
        actual: list[object], expected: list[object], message: str = ""
    ) -> None:
        assert actual == expected, (
            f"{message}. Actual list: {actual}, Expected list: {expected}"
        )
        
    @allure.step("Verify not equals")
    def verify_not_equals(
        actual: object, expected: object, message: str = ""
    ) -> None:
        assert actual != expected, (
            f"{message}. Actual: {actual}, Expected: {expected}"
        )
        
    @allure.step("Verify higher than")
    def verify_higher_than(
        num: int | float,
        threshold: int | float,
        message: str = ""
    ) -> None:
        assert num > threshold, (
            f"{message}. num: {num}, threshold: {threshold}"
        )

    @allure.step("Verify equals or higher than")
    def verify_equals_or_higher_than(
        num: int | float, threshold: int | float, message: str = ""
    ) -> None:
        assert num >= threshold, (
            f"{message}. num: {num}, threshold: {threshold}"
        )

    @allure.step("Verify lower than")
    def verify_lower_than(
        num: int | float, limit: int | float, message: str = ""
    ) -> None:
        assert num < limit, f"{message}. num: {num}, limit: {limit}"

    @allure.step("Verify equals or higher than")
    def verify_equals_or_lower_than(
        num: int | float, limit: int | float, message: str = ""
    ) -> None:
        assert num <= limit, f"{message}. num: {num}, limit: {limit}"

    @allure.step("Verify date format")
    def verify_date_format(date: str, format: str, message: str = "") -> None:
        assert datetime.strptime(
            date, format
        ), (
            f"{message}. Actual: {date}, "
            f"Expected format: {format}"
        )

    @allure.step("Verify in list")
    def verify_in_list(
        actual: object, expected: list[object], message: str = ""
    ) -> None:
        assert actual in expected, (
            f"{message}. Actual: {actual}, Expected: {expected}"
        )

    @allure.step("Verify element clickable")
    def verify_element_clickable(element: WebElement) -> None:
        assert element.is_enabled() is True, "Element is not clickable"