from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from time import sleep

class AddToCart:
    def __init__(self, driver):
        self.driver = driver
        self.url = "https://www.chitai-gorod.ru/"
        self.wait = WebDriverWait(driver, 10)

        # Локаторы
        self.popup_locator = (By.CSS_SELECTOR, ".tippy-box")
        self.close_button_locator = (By.CSS_SELECTOR, ".chg-app-button")
        self.buy_button_locator = (By.CSS_SELECTOR, "button[aria-label='false']")
        self.cart_button_locator = (By.CSS_SELECTOR, ".header-cart__icon, button[aria-label='Корзина']")
        self.search_input_locator = (By.CSS_SELECTOR, "input.search-form__input")

    def open(self):
        """Открывает страницу"""
        self.driver.get(self.url)
        self.close_popup()
        return self
    
    def close_popup(self):
        """Закрывает всплывающее окно, если оно появилось"""
        try:
            popup = self.wait.until(
                EC.visibility_of_element_located(self.popup_locator)
            )
            close_button = popup.find_element(*self.close_button_locator)
            close_button.click()
            self.wait.until(
                EC.invisibility_of_element_located(self.popup_locator)
            )
            print("✅ Всплывающее окно успешно закрыто")
            return self
        except Exception as e:
            print(f"Всплывающее окно не появилось или не удалось закрыть: {e}")

    def find_element(self, locator):
        """Находит элемент на странице"""
        return self.wait.until(EC.visibility_of_element_located(locator))

    def enter_text_and_submit(self, text):
        """Пишем в строку поиска и нажимаем Enter"""
        try:
            search_field = self.find_element(self.search_input_locator)
            search_field.clear()
            search_field.send_keys(text)
            search_field.send_keys(Keys.ENTER)
            print(f"✅ Поиск выполнен: {text}")
            sleep(2)
            return self
        except Exception as e:
            print(f"❌ Ошибка при поиске: {e}")
            return self

    def wait_for_search_results(self):
        """Ожидает появления результатов поиска"""
        try:
            self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".products-list, .product-card, .search-results, [data-testid='search-results']"))
            )
            print("✅ Результаты поиска загружены")
            return True
        except Exception as e:
            print(f"Результаты не найдены: {e}")
            return False

    def get_results_count(self):
        results = self.driver.find_elements(By.CSS_SELECTOR, ".product-card, .search-result-item, [data-testid*='product']")
        count = len(results)        
        return count 

    def scroll_down(self, pixels=500):
        """Прокручивает страницу вниз на указанное количество пикселей"""
        self.driver.execute_script(f"window.scrollBy(0, {pixels});")
        print(f"✅ Прокрутка вниз на {pixels} пикселей")
        sleep(1)  
        return self

    def add_to_cart(self):
        """Добавляет товар в корзину"""
        try:
            # Ждем и кликаем по кнопке "Купить"
            buy_button = self.wait.until(
                EC.element_to_be_clickable(self.buy_button_locator)
            )
            
            # Прокручиваем к кнопке если нужно
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", buy_button)
            sleep(1)
            
            buy_button.click()
            print("✅ Товар добавлен в корзину")
            sleep(2)  # Ждем обновления корзины
            return True
            
        except Exception as e:
            print(f"❌ Не удалось добавить товар в корзину: {e}")
            return False

    def enter_cart(self):
        """Переходит в корзину"""
        try:
            # Ищем кнопку корзины
            cart_button = self.wait.until(
                EC.element_to_be_clickable(self.cart_button_locator)
            )

            # Прокручиваем страницу к кнопке
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", cart_button)
            print("✅ Прокрутили к кнопке корзины")
            sleep(1)
            
            # Кликаем
            cart_button.click()
            print("✅ Переход в корзину выполнен")
            
            # Ждем загрузки страницы корзины
            self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".cart-page, .basket, [class*='cart']"))
            )
            print("✅ Страница корзины загружена")
            sleep(2)
            return True
            
        except Exception as e:
            print(f"❌ Не удалось перейти в корзину: {e}")
            return False