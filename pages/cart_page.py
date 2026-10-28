import json
import allure

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage, DEFAULT_TIMEOUT
from components.header import HeaderComponent
from selenium.webdriver.common.by import By
from pages.orders_page import OrdersPage
from selenium.common.exceptions import TimeoutException

class CartPage(BasePage):

    CART_PRODUCTS_LOCATOR = (By.CSS_SELECTOR, "div[id='cart-content'] > div:first-child > div")
    PROMO_INPUT_LOCATOR = (By.ID, "promo-input")
    PROMO_BTN_LOCATOR = (By.CSS_SELECTOR, "button[onclick='applyPromo()']")
    # Для итоговой суммы нет более конкретного локатора, ждём пока сделают =)
    DISCOUNT_SUM_LOCATOR = (By.CSS_SELECTOR, "div[id='cart-content'] > div:last-child > div:nth-child(3) > div:nth-child(2) > span:nth-child(2)")
    FINAL_SUM_LOCATOR = (By.CSS_SELECTOR, "div[id='cart-content'] > div:last-child > div > div:last-child > span:last-child")
    PROMO_MARK_LOCATOR = (By.CSS_SELECTOR, "div[id='cart-content'] > div:last-child > div:nth-child(3) > div:nth-child(2)")
    CHECKOUT_BUTTON_LOCATOR = (By.CSS_SELECTOR, "button[onclick='checkout()']")

    PATH = "/cart"

    def __init__(self, driver, base_url = None):
        super().__init__(driver, base_url) if base_url else super().__init__(driver)
        self.header = HeaderComponent(driver)

    @allure.step("Открытие страницы Корзина")
    def open(self):
        return super().open(self.PATH)

    @allure.step("Получение количества товаров в корзине")
    def get_items_count(self) -> int:
        products = self.find_all(self.CART_PRODUCTS_LOCATOR)
        return len(products)

    @allure.step("Получение количества товаров в корзине через localStorage")
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

    @allure.step("Ожидание, пока в счетчике корзины не окажется {expected_count}")
    def wait_for_cart_count(self, expected_count: int, timeout=10):
        return self.wait_until(
            lambda driver: self.header.get_cart_count() == expected_count,
            timeout=timeout
        )

    @allure.step("Ожидание, пока в корзине не окажется {expected_count} товаров")
    def wait_for_items_count(self, expected_count: int):
        return self.wait_until(
            lambda _: len(self.driver.find_elements(*self.CART_PRODUCTS_LOCATOR))
            if len(self.driver.find_elements(*self.CART_PRODUCTS_LOCATOR)) >= expected_count
            else False
        )

    @allure.step("Применение промокода {code} и ожидание изменения итоговой стоимости")
    def apply_promo_and_wait(self, code: str, old_total: str):
        self.apply_promo(code)

        self.wait_until(
            lambda _: self.get_total() != old_total
        )

    @allure.step("Применение промокода {code}")
    def apply_promo(self, code):
        self.type_text(self.PROMO_INPUT_LOCATOR, code)
        self.click(self.PROMO_BTN_LOCATOR)

    @allure.step("Получение итоговой стоимости")
    def get_total(self) -> str:
        return self.get_text(self.FINAL_SUM_LOCATOR)

    @allure.step("Получение значения скидки")
    def get_discount(self):
        return self.get_text(self.DISCOUNT_SUM_LOCATOR)

    @allure.step("Оформление заказа")
    def checkout(self) -> "OrdersPage":
        self.click(self.CHECKOUT_BUTTON_LOCATOR)
        alert_name = WebDriverWait(self.driver, 10).until(EC.alert_is_present())
        alert_name.send_keys("Name")
        alert_name.accept()
        alert_phone = WebDriverWait(self.driver, 10).until(EC.alert_is_present())
        alert_phone.send_keys("8800")
        alert_phone.accept()
        alert_address = WebDriverWait(self.driver, 10).until(EC.alert_is_present())
        alert_address.send_keys("Address")
        alert_address.accept()
        final_alert = WebDriverWait(self.driver, 10).until(EC.alert_is_present())
        final_alert.accept()

        orders = OrdersPage(self.driver)
        orders.wait_for_url_contains("/orders")
        return orders

    @allure.step("Проверка видимости скидки")
    def is_visible_discount(self, timeout = 3):
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(self.DISCOUNT_SUM_LOCATOR)
            )
            return True
        except TimeoutException:
            return False
