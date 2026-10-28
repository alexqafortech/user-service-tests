import time
import json
import allure

from pages.base_page import BasePage
from components.header import HeaderComponent
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

class CatalogPage(BasePage):

    PRODUCT_CARD = (By.CSS_SELECTOR, "#products-grid > div")
    ADD_TO_CART_BTN = (By.XPATH, ".//button[contains(text(), 'В корзину')]")
    CART_COUNTER = (By.CSS_SELECTOR, "a[href='/cart'] > span")
    IPHONE_ITEM = (By.CSS_SELECTOR, "a[href='/product/1']")
    FIRST_CARD = (By.CSS_SELECTOR, "#products-grid > div:first-child > a")
    PATH = "/catalog"

    def __init__(self, driver, base_url = None):
        super().__init__(driver, base_url) if base_url else super().__init__(driver)
        self.header = HeaderComponent(driver)

    @allure.step("Открытие страницы Каталог")
    def open(self):
        return super().open(self.PATH)

    @allure.step("Получение товаров")
    def get_products(self):
        return WebDriverWait(self.driver, 10).until(
            lambda d: d.find_elements(*self.PRODUCT_CARD)
            if len(d.find_elements(*self.PRODUCT_CARD)) >= 5
            else False
        )

    @allure.step("Добавление первого товара в корзину")
    def add_first_product_to_cart(self):
        self.click(self.ADD_TO_CART_BTN)

    @allure.step("Добавление товара {index} в корзину")
    def add_product_to_cart(self, index: int):
        products = self.get_products()
        time.sleep(0.15)
        products[index].find_element(*self.ADD_TO_CART_BTN).click()
        time.sleep(0.15)
        self.alert_accept()

    @allure.step("Ожидание пока значение счетчика корзины не станет {expected_count}")
    def wait_for_cart_count(self, expected_count: int):
        return self.wait_until(
            lambda _: self.header.get_cart_count()
            if self.header.get_cart_count() == expected_count
            else False
        )

    @allure.step("Получение количества товаров из localStorage")
    def get_localstorage_cart_count(self) -> int:
        data = self.driver.execute_script(
            "return localStorage.getItem('cart_items')"
        )

        if not data or data == "null":
            return 0

        return len(json.loads(data))

    @allure.step("Очистка localStorage")
    def clear_localstorage_cart(self):
        self.driver.execute_script(
            "localStorage.removeItem('cart_items')"
        )

    @allure.step("Добавление товара {index} в корзину и принятие окна alert")
    def add_product_to_cart_and_wait(self, index: int, expected_count: int):
        products = self.get_products()

        products[index].find_element(*self.ADD_TO_CART_BTN).click()
        self.alert_accept()
        self.wait_for_cart_count(expected_count)