from selenium.webdriver.common.by import By

class ProductCard:
    PRODUCT_CARD = (By.CSS_SELECTOR, "#products-grid > div")
    TITLE = (By.CSS_SELECTOR, "div.p-4 h3")
    PRICE = (By.CSS_SELECTOR, "div.p-4 > p")
    ADD_BTN = (By.CSS_SELECTOR, "div.p-4 > button")

    def __init__(self, driver, index):
        self.driver = driver
        self.index = index

    def _get_root(self):
        cards = self.driver.find_elements(*self.PRODUCT_CARD)
        return cards[self.index]

    def get_title(self):
        return self._get_root().find_element(*self.TITLE).text.strip()

    def get_price(self):
        return self._get_root().find_element(*self.PRICE).text.strip()

    def add_to_cart(self):
        self._get_root().find_element(*self.ADD_BTN).click()