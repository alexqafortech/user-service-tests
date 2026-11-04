
import allure

from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class OrdersPage(BasePage):
    PATH = "/orders"

    ORDER_ROW = (By.XPATH, "//a[contains(@href, '/orders/')]")
    ORDER_STATUS = (By.XPATH, "//span[contains(@class, 'status')]")

    def __init__(self, driver, base_url=None):
        if base_url:
            super().__init__(driver, base_url)
        else:
            super().__init__(driver)

    @allure.step("Открытие страницы заказов")
    def open(self):
        return super().open(self.PATH)

    @allure.step("Получение количества заказов")
    def get_order_count(self) -> int:
        return len(self.driver.find_elements(*self.ORDER_STATUS))
