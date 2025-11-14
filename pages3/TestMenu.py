from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from time import sleep

class TestMenu:
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

        # Локаторы для кнопок меню
        self.promotions_button_locator = (By.XPATH, "//li[@class='header-menu__item']//span[text()='Акции']/parent::a")
        self.sales_button_locator = (By.XPATH, "//li[@class='header-menu__item']//span[text()='Распродажа']/parent::a")
        self.certificate_button_locator = (By.XPATH, "//li[@class='header-menu__item']//span[text()='Сертификаты']/parent::a")
        self.bonusprogram_button_locator = (By.XPATH, "//li[@class='header-menu__item']//span[text()='Программа лояльности ']/parent::a")
        self.articles_button_locator = (By.XPATH, "//li[@class='header-menu__item']//span[text()='Блог']/parent::a")
        self.mainpage_button_locator = (By.CSS_SELECTOR, ".header-sticky__logo-link")

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

    def find_clickable_element(self, locator):
        """Находит кликабельный элемент"""
        return self.wait.until(EC.element_to_be_clickable(locator))

    def click_menu_item(self, locator, item_name):
        """Кликает на пункт меню и проверяет переход"""
        try:
            # Находим и кликаем на элемент
            element = self.find_clickable_element(locator)
            original_url = self.driver.current_url  # Сохраняем исходный URL
            
            element.click()
            print(f"✅ Клик на '{item_name}' выполнен")
            
            # Ждем загрузки новой страницы
            sleep(3)
            
            # Проверяем, что URL изменился
            current_url = self.driver.current_url
            if current_url != original_url:
                print(f"✅ Успешный переход на страницу '{item_name}'")
                print(f"🔗 Новый URL: {current_url}")
                return True
            else:
                print(f"⚠️ URL не изменился после клика на '{item_name}'")
                return False
                
        except Exception as e:
            print(f"❌ Ошибка при клике на '{item_name}': {e}")
            return False

    def test_promotions_button(self):
        """Тестирует кнопку 'Акции'"""
        return self.click_menu_item(self.promotions_button_locator, "Акции")

    def test_sales_button(self):
        """Тестирует кнопку 'Распродажа'"""
        return self.click_menu_item(self.sales_button_locator, "Распродажа")

    def test_certificate_button(self):
        """Тестирует кнопку 'Сертификаты'"""
        return self.click_menu_item(self.certificate_button_locator, "Сертификаты")

    def test_bonusprogram_button(self):
        """Тестирует кнопку 'Программа лояльности'"""
        return self.click_menu_item(self.bonusprogram_button_locator, "Программа лояльности")

    def test_articles_button(self):
        """Тестирует кнопку 'Блог'"""
        return self.click_menu_item(self.articles_button_locator, "Блог")

    def test_all_menu_items_independent(self):
        """Тестирует все пункты меню независимо друг от друга"""
        print("🚀 Начинаем независимое тестирование пунктов меню...")
        
        results = {}
        
        # Для каждого теста создаем новый драйвер
        menu_items = [
            ("Акции", self.promotions_button_locator),
            ("Распродажа", self.sales_button_locator),
            ("Сертификаты", self.certificate_button_locator),
            ("Программа лояльности", self.bonusprogram_button_locator),
            ("Блог", self.articles_button_locator)
        ]
        
        for item_name, locator in menu_items:
            print(f"\n🔍 Тестируем: {item_name}")
            
            try:
                # Каждый тест начинается с чистой страницы
                self.driver.get(self.url)
                self.close_popup()
                sleep(2)
                
                # Выполняем тест
                success = self.click_menu_item(locator, item_name)
                results[item_name] = success
                
            except Exception as e:
                print(f"❌ Критическая ошибка при тесте '{item_name}': {e}")
                results[item_name] = False
        
        # Выводим итоги
        print("\n📊 РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ:")
        for item, result in results.items():
            status = "✅ УСПЕХ" if result else "❌ ОШИБКА"
            print(f"  {item}: {status}")
        
        # Проверяем общий результат
        all_passed = all(results.values())
        if all_passed:
            print("🎉 Все тесты прошли успешно!")
        else:
            failed_items = [item for item, result in results.items() if not result]
            print(f"⚠️ Проблемы с пунктами: {', '.join(failed_items)}")
        
        return all_passed

    def test_single_menu_item(self, item_name, locator):
        """Тестирует один пункт меню независимо"""
        print(f"\n🔍 Тестируем: {item_name}")
        
        try:
            # Начинаем с чистой страницы
            self.driver.get(self.url)
            self.close_popup()
            sleep(2)
            
            # Выполняем тест
            success = self.click_menu_item(locator, item_name)
            
            if success:
                print(f"🎉 {item_name} - РАБОТАЕТ")
            else:
                print(f"❌ {item_name} - НЕ РАБОТАЕТ")
                
            return success
            
        except Exception as e:
            print(f"❌ Критическая ошибка при тесте '{item_name}': {e}")
            return False

    def get_current_url(self):
        """Возвращает текущий URL"""
        return self.driver.current_url

    def get_page_title(self):
        """Возвращает заголовок страницы"""
        return self.driver.title