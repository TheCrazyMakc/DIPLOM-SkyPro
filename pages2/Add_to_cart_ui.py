from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import allure
from time import sleep


class AddCart:
  def __init__(self, driver):
        """Базовый класс для всех страниц"""
        self.driver = driver
        self.url = "https://www.chitai-gorod.ru/"
        self.wait = WebDriverWait(driver, 10)

  @allure.step("Переход в корзину")
  def enter_cart(self):
      """Переходит в корзину через кнопку в header"""
      try:
          # Локатор для кнопки корзины
          cart_button = self.find_element((By.CSS_SELECTOR, 'button.header-controls__btn[aria-label="Корзина"]'))
          print("✅ Кнопка корзины найдена")
          
          # Прокручиваем страницу к кнопке
          self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", cart_button)
          print("✅ Прокрутили к кнопке корзины")
          sleep(1)
          
          # Ждем пока кнопка станет кликабельной
          self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.header-controls__btn[aria-label="Корзина"]')))
          
          # Пробуем кликнуть через JavaScript если обычный клик не работает
          try:
              cart_button.click()
          except:
              self.driver.execute_script("arguments[0].click();", cart_button)
              print("✅ Клик через JavaScript выполнен")
          
          print("✅ Кнопка корзины нажата")
          
          # Ждем загрузки страницы корзины
          self.wait.until(
              EC.presence_of_element_located((By.CSS_SELECTOR, ".cart-page__title"))
          )
          print("✅ Страница корзины загружена")
          sleep(2)
          return self
          
      except Exception as e:
          print(f"❌ Ошибка при переходе в корзину: {e}")
          return self