from selenium import webdriver
from selenium.webdriver.common.by import By
import allure
from pages.Search_by_name_ui import SearchByAuthor
from pages.Add_to_cart_ui import AddToCart
from pages.Delete_from_cart_ui import DeleteFromCart
from constants import UI_url

search_by_author = SearchByAuthor
add_to_card = AddToCart
delete_from_cart = DeleteFromCart

@allure.title("Тест поиска книг по автору. POSITIVE")
@allure.description("Этот тест проверяет, что поиск книг по автору работает корректно.")
@allure.feature("READ")
@allure.severity("CRITICAL")
def test_search_by_author ():
        """ 
                          Проверка корректности результатов поиска по автору.
                          
        """
        with allure.step ("Запустить браузер Chrome"):
            driver = webdriver.Chrome() 
       
        with allure.step ("Перейти на сайт Читай-город"):
            driver.get(UI_url)  

        with allure.step ("Найти книгу по автору Сумейе Коч"):
            author_name = "Сумейе Коч"
            search_by_author(author_name)
        
        with allure.step ("Получить результаты поиска"):
            results_find = driver.find_element(By.CLASS_NAME, "product-title__author")

        with allure.step ("Проверить, что поиск по автору успешен"):
            assert results_find is not None
    
        with allure.step ("Закрыть браузер"):
            driver.quit()  

@allure.title("Тест добавления товара в корзину. POSITIVE")
@allure.description("Этот тест проверяет, что товар добавляется в корзину.")
@allure.feature("CREATE")
@allure.severity("BLOCKER")
def test_add_to_card():
        """
                             Проверка корректности добавления товара в корзину.
                             
        """
        with allure.step ("Запустить браузер Chrome"):
            driver = webdriver.Chrome() 
        
        with allure.step ("Перейти на сайт Читай-город"):
            driver.get(UI_url)  

        with allure.step ("Добавить в корзину книгу с названием Ветреный"):
            book_title = "Ветреный"
            add_to_card(book_title)
        
        with allure.step ("Получить результаты добавления в корзину"):
            results_add = driver.find_element(By.CSS_SELECTOR, 'div.product-title__head')

        with allure.step ("Проверить, что корзина не пуста"):
            assert results_add is not None
               
        with allure.step ("Закрыть браузер"):
            driver.quit() 

@allure.title("Тест удаления товара из корзины. POSITIVE")
@allure.description("Этот тест проверяет, что товар из корзины удаляется корректно.")
@allure.feature("DELETE")
@allure.severity("BLOCKER")
def test_delete_from_card():
        """
                             Проверка корректности удаления товара из корзины.
                             
        """

        with allure.step ("Запустить браузер Chrome"):
            driver = webdriver.Chrome() 
        
        with allure.step ("Перейти на сайт Читай-город"):
            driver.get(UI_url)  


        with allure.step ("Удалить книгу из корзины"):
            book_title = "Ветреный"
            delete_from_cart(book_title)
            results_del = driver.find_elements(By.CSS_SELECTOR, 'div.product-title__head')

        with allure.step ("Проверить, что товар больше не существует в списке"):
            assert all(book_title not in element.text for element in results_del), f"Книга '{book_title}' все еще в корзине."
