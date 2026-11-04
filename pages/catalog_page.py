
import json
import allure

from pages.base_page import BasePage
from components.header import HeaderComponent
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC


class CatalogPage(BasePage):

    PRODUCT_CARD = (By.CSS_SELECTOR, "#products-grid > div")
    ADD_TO_CART_BTN = (
        By.XPATH,
        ".//button[contains(text(), 'В корзину')]"
    )
    CART_COUNTER = (By.CSS_SELECTOR, "a[href='/cart'] > span")
    IPHONE_ITEM = (By.CSS_SELECTOR, "a[href='/product/1']")
    FIRST_CARD = (
        By.CSS_SELECTOR,
        "#products-grid a[href='/product/1'] img"
    )

    PATH = "/catalog"

    def __init__(self, driver, base_url=None):
        super().__init__(driver, base_url) if base_url else super().__init__(driver)
        self.header = HeaderComponent(driver)

    @allure.step("Открытие страницы Каталог")
    def open(self):
        return super().open(self.PATH)

    @allure.step("Получение товаров")
    def get_products(self):
        def products_loaded(driver):
            products = driver.find_elements(*self.PRODUCT_CARD)
            return products if len(products) >= 5 else False

        return WebDriverWait(self.driver, 10).until(products_loaded)

    @allure.step("Добавление первого товара в корзину")
    def add_first_product_to_cart(self):
        self.add_product_to_cart(0)

    @allure.step("Добавление товара {index} в корзину")
    def add_product_to_cart(self, index: int):
        products = self.get_products()

        button = products[index].find_element(
            By.CSS_SELECTOR,
            "button[onclick*='addToCart']"
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            button
        )

        button.click()

        alert = WebDriverWait(self.driver, 5).until(
            EC.alert_is_present()
        )

        alert.accept()

    @allure.step(
        "Ожидание пока значение счетчика корзины не станет {expected_count}"
    )
    def wait_for_cart_count(self, expected_count: int, timeout=5):
        return self.wait_until(
            lambda _: (
                count
                if (count := self.header.get_cart_count()) == expected_count
                else False
            ),
            timeout=timeout
        )

    @allure.step("Добавление товара {index} в корзину и ожидание счетчика")
    def add_product_to_cart_and_wait(
        self,
        index: int,
        expected_count: int
    ):
        self.add_product_to_cart(index)
        self.wait_for_cart_count(expected_count)

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
