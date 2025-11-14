from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from pages3.TestMenu import TestMenu

def test_with_simple_maximize():
    """Простой способ с maximize_window()"""
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    
    # Развернуть окно
    driver.maximize_window()
    print("✅ Браузер развернут на весь экран")
    
    try:
        menu_tester = TestMenu(driver)
        menu_tester.test_all_menu_items_independent()
    finally:
        driver.quit()

if __name__ == "__main__":
    test_with_simple_maximize()