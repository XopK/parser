import time
import sys
import os
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd

output_folder = 'output'
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Укажите путь к Microsoft Edge WebDriver
if getattr(sys, 'frozen', False):  # Если программа запущена как .exe
    driver_path = os.path.join(sys._MEIPASS, 'driver', 'msedgedriver.exe')
else:  # Если программа запущена как обычный скрипт
    driver_path = r"driver\msedgedriver.exe"

# Создаем объект Service для EdgeDriver
service = Service(executable_path=driver_path)

# URL страницы, которую будем парсить
url = "https://malakhit-spb.ru/pamyatniki"

# Настраиваем Selenium с EdgeDriver
driver = webdriver.Edge(service=service)
driver.set_window_size(1920, 1080)

# Открываем страницу
driver.get(url)

# Настраиваем явное ожидание
wait = WebDriverWait(driver, 10)

data = []

# Цикл для загрузки всех карточек с товаров
while True:
    try:
        # Ищем кнопку "Загрузить еще"
        load_more_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'js-store-load-more-btn')))
        load_more_button.click()  # Кликаем на кнопку

        # Ждем, пока новые карточки загрузятся
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.t-store__card')))

        time.sleep(2)  # Ждем между кликами для надежности
    except Exception as e:
        print("Кнопка 'Загрузить еще' больше не доступна или возникла ошибка:", e)
        break

# После завершения загрузки всех данных получаем HTML-код страницы
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

# Ищем карточки товаров
products = soup.find_all('div', class_='t-store__card')

for product in products:
    # Название товара
    title = product.find('div', class_='t-store__card__title').get_text(strip=True) if product.find('div',
                                                                                                    class_='t-store__card__title') else None

    # Категория товара (очистка от фразы "Бесплатная доставка по СПб")
    description_tag = product.find('div', class_='t-store__card__descr')
    description = description_tag.get_text(strip=True).replace("Бесплатная доставка по СПб",
                                                               "").strip() if description_tag else None

    # Парсинг цены
    price_tag = product.find('div', class_='js-product-price')
    if price_tag:
        price_str = price_tag.get_text(strip=True).replace(" ", "").replace("р.", "")
        try:
            price = int(price_str)
        except ValueError:
            price = 'Цена отсутствует'
    else:
        price = None

    # URL изображения
    image_tag = product.find('img', class_='t-store__card__img')
    image_url = image_tag.get('data-original') if image_tag else None

    # Извлекаем ссылку на товар
    link_tag = product.find('a', href=True)
    if link_tag:
        product_link = link_tag['href']

        # Переходим на страницу товара
        driver.get(product_link)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.js-store-prod-charcs')))  # Ждем загрузки

        # Получаем HTML страницы товара
        product_page_html = driver.page_source
        product_soup = BeautifulSoup(product_page_html, 'html.parser')

        # Характеристики товара
        characteristics = product_soup.find_all('p', class_='js-store-prod-charcs')
        elements = [char.get_text(strip=True) for char in characteristics]

        # Возвращаемся назад
        driver.back()
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.t-store__card')))  # Ждем загрузки страницы

    else:
        elements = None

    # Добавляем собранные данные
    data.append([title, description, price, image_url, elements])

# Закрываем браузер
driver.quit()

# Создаем DataFrame и сохраняем в Excel
df = pd.DataFrame(data, columns=['Название', 'Описание', 'Цена', 'Ссылка на изображение', 'Элементы'])
df.to_excel(f'{output_folder}/products_data.xlsx', index=False)
print(f"Данные успешно сохранены в файл {output_folder}/products_data.xlsx")
