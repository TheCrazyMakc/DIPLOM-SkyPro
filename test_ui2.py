import allure
from pages2.Main_page_ui import BasePage 
from pages2.Search_by_name_ui import SearchPage 
from pages2.Add_to_cart_ui import AddCart 
from time import sleep

def open_page():
    """Запускающая функция для тестирования класса BasePage"""
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager
    
    # Инициализация драйвера
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    
    try:
        # Создание экземпляра страницы
        page = BasePage(driver)
        
        # Открытие страницы и автоматическое закрытие попапа
        page.open()        
        print("✅ Страница успешно открыта и попап обработан")

    except Exception as e:
        print(f"Произошла ошибка: {e}")
        # Прикрепляем скриншот при ошибке
        allure.attach(driver.get_screenshot_as_png(), name="Ошибка", attachment_type=allure.attachment_type.PNG)
        raise e
        
    finally:
        # Закрытие браузера
        driver.quit()
        print("Браузер закрыт")


# def search_name():
    


if __name__ == "__main__":
    open_page()