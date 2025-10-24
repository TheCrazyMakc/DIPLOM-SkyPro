from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import allure
from time import sleep


class BasePage:
    def __init__(self, driver):
        """Базовый класс для всех страниц"""
        self.driver = driver
        self.url = "https://www.chitai-gorod.ru/"
        self.wait = WebDriverWait(driver, 10)

        # Локаторы для всплывающего окна и кнопки
        self.popup_locator = (By.CSS_SELECTOR, ".tippy-box")
        self.close_button_locator = (By.CSS_SELECTOR, ".chg-app-button")
        self.bay_button_locator = (By.CSS_SELECTOR, ".chg-app-button__content")

    def open(self):
        """Открывает страницу"""
        self.driver.get(self.url)
        self.close_popup()
        return self
    
    def close_popup(self):
        """Закрывает всплывающее окно, если оно появилось"""
        try:
            # Ждем появления всплывающего окна
            popup = self.wait.until(
                EC.visibility_of_element_located(self.popup_locator)
            )
            
            # Ищем кнопку внутри всплывающего окна
            close_button = popup.find_element(*self.close_button_locator)
            
            # Нажимаем кнопку
            close_button.click()
            
            # Ждем исчезновения всплывающего окна
            self.wait.until(
                EC.invisibility_of_element_located(self.popup_locator)
            )
            
            print("✅ Всплывающее окно успешно закрыто")
            return self
        
        except Exception as e:
            print(f"Всплывающее окно не появилось или не удалось закрыть: {e}")