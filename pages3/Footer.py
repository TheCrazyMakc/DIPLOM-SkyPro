from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from time import sleep
import time

class Footer:
    def __init__(self, driver):
        """Класс для тестирования меню на сайте"""
        self.driver = driver
        self.url = "https://www.chitai-gorod.ru/"
        self.wait = WebDriverWait(driver, 10)

        # Развернуть окно при инициализации
        self.driver.maximize_window()

        # Локаторы для всплывающего окна
        self.popup_locator = (By.CSS_SELECTOR, ".tippy-box")
        self.close_button_locator = (By.CSS_SELECTOR, ".chg-app-button")

        # Локаторы для кнопок социальных сетей
        self.social_locators = {
            "vk": (By.CSS_SELECTOR, 'a.app-social-links__icon[href*="vk.com/chitaigorod"]'),
            "ok": (By.CSS_SELECTOR, 'a.app-social-links__icon[href*="ok.ru/chitaigorod"]'),
            "youtube": (By.CSS_SELECTOR, 'a.app-social-links__icon[href*="youtube.com/channel/UCbsqXVnwSqer9QttshVs76A"]'),
            "tiktok": (By.CSS_SELECTOR, 'a.app-social-links__icon[href*="tiktok.com/@chitai_gorod"]'),
            "telegram": (By.CSS_SELECTOR, 'a.app-social-links__icon[href*="t.me/chitai_gorod_official"]')
        }

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

    def scroll_to_bottom(self, scroll_pause_time=2):
        """Скроллит страницу до самого низа"""
        # Получаем начальную высоту страницы
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        
        while True:
            # Скроллим до текущего низа
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            
            # Ждем загрузки нового контента
            time.sleep(scroll_pause_time)
            
            # Получаем новую высоту
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            
            # Если высота не изменилась - достигли дна
            if new_height == last_height:
                break
                
            last_height = new_height
        print("✅ Страница проскроллена до низа")

    def test_social_links_clickable(self):
        """Проверяет кликабельность всех социальных кнопок с возвратом на исходную страницу"""
        # Запоминаем исходную вкладку
        original_window = self.driver.current_window_handle
        
        for social_name, locator in self.social_locators.items():
            try:
                print(f"\n--- Проверяем {social_name.upper()} ---")
                
                # Ищем элемент
                element = self.wait.until(
                    EC.element_to_be_clickable(locator)
                )
                print(f"✅ Кнопка {social_name} найдена и кликабельна")
                
                # Получаем URL для информации
                href = element.get_attribute('href')
                print(f"🔗 Ссылка: {href}")
                
                # Кликаем на кнопку (откроется в новой вкладке)
                element.click()
                sleep(2)
                
                # Ждем открытия новой вкладки
                self.wait.until(EC.number_of_windows_to_be(2))
                
                # Переключаемся на новую вкладку
                new_window = [window for window in self.driver.window_handles if window != original_window][0]
                self.driver.switch_to.window(new_window)
                
                # Проверяем, что мы перешли на правильную страницу
                current_url = self.driver.current_url
                print(f"📄 Открыта страница: {current_url}")
                print(f"📝 Заголовок: {self.driver.title}")
                
                # Закрываем новую вкладку
                self.driver.close()
                
                # Возвращаемся на исходную вкладку
                self.driver.switch_to.window(original_window)
                print(f"✅ Возврат на исходную страницу: {self.driver.current_url}")
                
            except Exception as e:
                print(f"❌ Ошибка при проверке {social_name}: {e}")
                # В случае ошибки убеждаемся, что мы на исходной вкладке
                if len(self.driver.window_handles) == 1:
                    self.driver.switch_to.window(original_window)
                elif len(self.driver.window_handles) > 1:
                    # Закрываем все лишние вкладки и возвращаемся к исходной
                    for window in self.driver.window_handles:
                        if window != original_window:
                            self.driver.switch_to.window(window)
                            self.driver.close()
                    self.driver.switch_to.window(original_window)

    def test_social_links_without_navigation(self):
        """Проверяет кликабельность без перехода по ссылкам (быстрая проверка)"""
        print("\n=== БЫСТРАЯ ПРОВЕРКА КЛИКАБЕЛЬНОСТИ ===")
        
        for social_name, locator in self.social_locators.items():
            try:
                element = self.wait.until(
                    EC.element_to_be_clickable(locator)
                )
                href = element.get_attribute('href')
                print(f"✅ {social_name.upper()}: кликабельна | {href}")
                
            except Exception as e:
                print(f"❌ {social_name.upper()}: не кликабельна - {e}")