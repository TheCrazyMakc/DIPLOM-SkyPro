import allure
from pages2.Main_page_ui import BasePage 
from pages2.Search_by_name_ui import SearchPage 
from pages2.Add_to_cart_ui import AddCart 
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


class TestRunner:
    def __init__(self):
        """Инициализация драйвера и страниц"""
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.base_page = BasePage(self.driver)
        self.search_page = SearchPage(self.driver)
        self.cart_page = AddCart(self.driver)
    
    @allure.step("Открытие главной страницы")
    def open_page(self):
        """Открывает главную страницу и закрывает попап"""
        try:
            self.base_page.open()        
            print("✅ Страница успешно открыта и попап обработан")
            return True
        except Exception as e:
            print(f"❌ Ошибка при открытии страницы: {e}")
            allure.attach(self.driver.get_screenshot_as_png(), name="Ошибка открытия", attachment_type=allure.attachment_type.PNG)
            return False

    @allure.step("Поиск товара по названию: {search_text}")
    def search_name(self, search_text="Python"):
        """Выполняет поиск товара по названию"""
        try:
            # Используем метод из SearchPage для поиска
            self.search_page.enter_text_and_submit(search_text)
            
            # Ждем результаты поиска
            if self.search_page.wait_for_search_results():
                count = self.search_page.get_results_count()
                print(f"✅ Найдено товаров: {count}")
                return count > 0
            else:
                print("❌ Результаты поиска не загрузились")
                return False
                
        except Exception as e:
            print(f"❌ Ошибка при поиске: {e}")
            allure.attach(self.driver.get_screenshot_as_png(), name="Ошибка поиска", attachment_type=allure.attachment_type.PNG)
            return False

    @allure.step("Переход в корзину")
    def go_to_cart(self):
        """Переходит в корзину"""
        try:
            self.cart_page.enter_cart()
            print("✅ Успешно перешли в корзину")
            return True
        except Exception as e:
            print(f"❌ Ошибка при переходе в корзину: {e}")
            allure.attach(self.driver.get_screenshot_as_png(), name="Ошибка корзины", attachment_type=allure.attachment_type.PNG)
            return False

    @allure.step("Полный сценарий тестирования")
    def run_full_test(self):
        """Запускает полный сценарий тестирования"""
        try:
            print("🚀 Запуск полного тестового сценария...")
            
            # Шаг 1: Открытие главной страницы
            if not self.open_page():
                return False
            sleep(2)
            
            # Шаг 2: Поиск товара
            if not self.search_name("Программирование"):
                return False
            sleep(2)
            
            # Шаг 3: Переход в корзину
            if not self.go_to_cart():
                return False
            sleep(2)
            
            print("🎉 Все тесты успешно пройдены!")
            return True
            
        except Exception as e:
            print(f"❌ Критическая ошибка в тестовом сценарии: {e}")
            allure.attach(self.driver.get_screenshot_as_png(), name="Критическая ошибка", attachment_type=allure.attachment_type.PNG)
            return False

    def close(self):
        """Закрывает браузер"""
        self.driver.quit()
        print("🔚 Браузер закрыт")


def open_page():
    """Отдельная функция для тестирования только открытия страницы"""
    runner = TestRunner()
    try:
        result = runner.open_page()
        return result
    finally:
        runner.close()


def search_name():
    """Отдельная функция для тестирования только поиска"""
    runner = TestRunner()
    try:
        # Сначала открываем страницу
        if runner.open_page():
            # Затем выполняем поиск
            result = runner.search_name("JavaScript")
            return result
        return False
    finally:
        runner.close()


def full_test():
    """Запускает полный тестовый сценарий"""
    runner = TestRunner()
    try:
        result = runner.run_full_test()
        return result
    finally:
        runner.close()


if __name__ == "__main__":
    # full_test()
    # Можно запускать отдельные функции или полный тест
    
    print("1. Тестируем только открытие страницы:")
    open_page()
    
    print("\n2. Тестируем поиск:")
    search_name()
    
    print("\n3. Запускаем полный тест:")
    full_test()