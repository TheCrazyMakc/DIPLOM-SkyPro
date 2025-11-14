from pages3.Footer import Footer 
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep

def test_open_page():
    """Запускающая функция для тестирования класса Footer"""
    # Инициализация драйвера
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    
    try:
        # Создаем экземпляр страницы
        page = Footer(driver)

        # Открываем страницу и закрываем попап
        page.open()        
        print("✅ Страница успешно открыта и попап обработан")
        sleep(2)

        # Скроллим до footer
        page.scroll_to_bottom()
        sleep(2)

        # Вариант 1: Полная проверка с переходом по ссылкам
        print("\n" + "="*50)
        print("ПОЛНАЯ ПРОВЕРКА С ПЕРЕХОДОМ ПО ССЫЛКАМ")
        print("="*50)
        page.test_social_links_clickable()

        # Вариант 2: Быстрая проверка без перехода
        print("\n" + "="*50)
        print("БЫСТРАЯ ПРОВЕРКА БЕЗ ПЕРЕХОДА")
        print("="*50)
        page.test_social_links_without_navigation()

        print("\n🎉 Все проверки завершены успешно!")

    except Exception as e:
        print(f"❌ Произошла ошибка: {e}")
    
    finally:
        sleep(3)
        driver.quit()

# Запуск теста
if __name__ == "__main__":
    test_open_page()