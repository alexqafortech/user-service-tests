from pages.base_page import BasePage
from components.header import HeaderComponent
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoAlertPresentException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait

class AdminPage(BasePage):

    PATH = "/admin"
    USERS_TABLE = (By.CSS_SELECTOR, "#users-table > div > table > tbody > tr")
    ITEM = (By.XPATH, "//td[contains(., 'test_user')]/following-sibling::td[1]")
    BLOCK_USER = (By.XPATH, "//td[contains(text(), 'ivanov_d')]/following-sibling::td[5]/div/button[contains(text(), 'Заблокировать')]")
    ACTIVATE_USER = (By.XPATH, "//td[contains(text(), 'test_hard_pass')]/following-sibling::td[5]/div/button[contains(text(), 'Активировать')]")
    TEXT_BLOCK_LOCATOR = (By.XPATH, "//td[contains(text(), 'ivanov_d')]/following-sibling::td[3]")
    RELOAD_LOCATOR = (By.ID, "reset-db-btn")

    def __init__(self, driver, base_url = None):
        super().__init__(driver, base_url) if base_url else super().__init__(driver)
        self.header = HeaderComponent(driver)

    def open(self):
        return super().open(self.PATH)

    def reload_page(self):
        self.driver.refresh()

    def reload_data_base(self):
        self.click(self.RELOAD_LOCATOR)
        self.alert_accept()

    def activate_user(self, username="test_hard_pass"):
        locator = (
            By.XPATH,
            f"//td[contains(text(), '{username}')]/following-sibling::td/div/button[contains(text(), 'Активировать')]"
        )

        button = WebDriverWait(self.driver, 5).until(
            EC.visibility_of_element_located(locator)
        )

        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", button)

        button.click()

        # На Firefox падает без минимального ожидания
        try:
            WebDriverWait(self.driver, 0.01).until(EC.alert_is_present())
        except TimeoutException:
            pass

        try:
            alert = self.driver.switch_to.alert
            alert_text = alert.text
            alert.accept()
            raise RuntimeError(f"Бэкенд вернул ошибку при активации '{username}': {alert_text}")
        except NoAlertPresentException:
            pass