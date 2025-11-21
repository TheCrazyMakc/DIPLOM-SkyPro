from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from time import sleep


class SearchPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

        self.search_results_locator = (By.CSS_SELECTOR, ".product-card")
        self.buy_button_locator = (
            By.CSS_SELECTOR,
            "button.product-buttons__main-action")
        self.cart_button_locator = (
            By.XPATH, "//button[contains(., 'Корзина')]")   

    def find_element(self, locator):
        """Находит элемент на странице"""
        return self.wait.until(EC.visibility_of_element_located(locator))

    def enter_text_and_submit(self, text):
        """Пишем в строку поиска и нажимаем Enter"""
        # Локатор для поискового поля
        search_field = self.find_element((By.CSS_SELECTOR, "input.search-form__input"))
        search_field.clear()
        search_field.send_keys(text)
        # Нажимаем Enter вместо клика по кнопке
        search_field.send_keys(Keys.ENTER)
        sleep(2)
        return self

    def wait_for_search_results(self):
        """Ожидает появления результатов поиска"""
        # Ждем появления результатов (используем несколько возможных селекторов)
        self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".products-list, .product-card, .search-results, [data-testid='search-results']"))
        )
        print("✅ Результаты поиска загружены")

    def get_results_count(self):
        results = self.driver.find_elements(By.CSS_SELECTOR, ".product-card, .search-result-item, [data-testid*='product']")
        count = len(results)        
        return count     