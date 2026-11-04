
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class HeaderComponent(BasePage):
    LOGO_LOCATOR = (By.XPATH, "//a[contains(text(),'ШопМаркет')]")
    CATALOG_LOCATOR = (By.CSS_SELECTOR, "a[href='/catalog']")
    CART_LOCATOR = (By.CSS_SELECTOR, "a[href='/cart']")
    CART_COUNT_LOCATOR = (By.CSS_SELECTOR, "a[href='/cart'] > span")
    MENU_TRIGGER_LOCATOR = (By.CSS_SELECTOR, "div[class='relative group']")
    PROFILE_LOCATOR = (By.CSS_SELECTOR, "a[href='/profile']")
    LOGOUT_LOCATOR = (By.CSS_SELECTOR, "button[onclick='logout()']")

    def read_cart_count(self) -> int:
        value = self.driver.execute_script("""
            const badge = document.querySelector("a[href='/cart'] > span");
            return badge ? badge.textContent.trim() : "0";
        """)

        try:
            return int(value) if value else 0
        except (TypeError, ValueError):
            return 0

    def get_cart_count(self, timeout=3) -> int:
        return self.read_cart_count()

    def go_to_catalog(self):
        self.click(self.CATALOG_LOCATOR)

    def go_to_cart(self):
        self.click(self.CART_LOCATOR)

    def open_user_menu(self):
        trigger = self.find(self.MENU_TRIGGER_LOCATOR)
        ActionChains(self.driver).move_to_element(trigger).perform()

    def go_to_profile(self):
        self.open_user_menu()
        self.click(self.PROFILE_LOCATOR)

    def logout(self):
        self.open_user_menu()
        self.click(self.LOGOUT_LOCATOR)
