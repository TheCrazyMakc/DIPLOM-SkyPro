from pages3.AddToCart import AddToCart 
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep

def open_page():
    """Запускающая функция для тестирования класса AddToCart"""
    # Инициализация драйвера
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    
    try:
        # Создаем экземпляр страницы
        page = AddToCart(driver)

        # Открываем страницу и закрываем попап
        page.open()        
        print("✅ Страница успешно открыта и попап обработан")
        sleep(2)
        
        # ТЕСТИРОВАНИЕ ПОИСКА
        search_query = "Python"
        print(f"🔍 Выполняем поиск: {search_query}")
        
        # Выполняем поиск
        page.enter_text_and_submit(search_query)
        
        # Ждем результаты поиска
        if page.wait_for_search_results():
            results_count = page.get_results_count()
            print(f"📚 Найдено результатов: {results_count}")
            
            if results_count > 0:
                print("✅ Поиск выполнен успешно!")
                
                # Прокрутка и добавление в корзину
                print("🔄 Прокручиваем страницу...")
                page.scroll_down(800)
                sleep(2)
                
                print("🛒 Добавляем товар в корзину...")
                if page.add_to_cart():
                    print("✅ Товар успешно добавлен в корзину")
                    
                    print("📦 Переходим в корзину...")
                    if page.enter_cart():
                        print("🎉 Успешно! Товар в корзине")
                    else:
                        print("❌ Не удалось перейти в корзину")
                else:
                    print("❌ Не удалось добавить товар в корзину")
            else:
                print("⚠️ Результаты не найдены")
        else:
            print("❌ Не удалось дождаться результатов поиска")
            
        # Финальная задержка
        sleep(5)
        
    except Exception as e:
        print(f"❌ Произошла ошибка: {e}")
        # Можно сделать скриншот для отладки
        driver.save_screenshot("error_screenshot.png")
        print("📸 Скриншот ошибки сохранен как 'error_screenshot.png'")
        
    finally:
        # Всегда закрываем браузер
        driver.quit()
        print("✅ Браузер закрыт")

if __name__ == "__main__":
    print("🚀 Запуск основного теста...")
    open_page()