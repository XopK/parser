# Парсeр

## Установка

1. **Скачайте и установите Python:**  
   Если Python еще не установлен на вашем компьютере, скачайте и установите его
   с [официального сайта Python](https://www.python.org/).


2. **Установите Microsoft Edge WebDriver:**
    - Скачайте драйвер, совместимый с вашей версией браузера Microsoft Edge,
      с [официальной страницы](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/).
    - Поместите файл `msedgedriver.exe` в папку `driver` внутри вашего проекта или укажите другой путь в переменной
      `driver_path`.


3. **Установите необходимые библиотеки:**

   В терминале или командной строке выполните следующую команду для установки всех необходимых библиотек:

   ```bash
   pip install -r requirements.txt

## Настройка

1. **Путь к WebDriver:**
   Убедитесь, что путь к WebDriver (`msedgedriver.exe`) корректно указан в переменной `driver_path` в коде:

   ```python
   driver_path = r".\driver\msedgedriver.exe"

2. Путь к папке для сохранения файлов:
   Файлы Excel будут сохраняться в папку `output`. Если такой папки нет, она будет создана автоматически. Если нужно
   указать другую папку, измените переменную `output_folder`:

   ```python
   output_folder = 'output'

## Запуск скрипта

1. Откройте терминал или командную строку.
2. Перейдите в директорию с вашим проектом.
3. Запустите скрипт:

   ```bash
   python parser.py
   
После выполнения скрипта данные будут сохранены в файл products_data.xlsx в папке output.