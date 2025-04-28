from flask import Flask, request, jsonify, render_template, url_for # Добавьте url_for, если еще не импортировали где-то
from google.oauth2.service_account import Credentials
import gspread
import json
import os

# Исправленная строка инициализации Flask:
app = Flask(__name__,
            template_folder='templates', # Искать шаблоны в папке py/templates/
            static_folder='../static')  # Искать статику в папке SITE--/static/

# --- Налаштування ---
# Убедитесь, что путь к JSON файлу правильный относительно МЕСТА ЗАПУСКА скрипта
# Если запускаете из папки SITE--/, то путь будет 'py/hastle-homes-....json'
# Если запускаете из папки py/, то путь 'hastle-homes-....json'
# Использование абсолютного пути менее гибко, но сработает, если он верный.
CREDENTIALS_FILE = 'C:/Users/zyuzk/OneDrive/Desktop/ссаный сайт/Site--/py/hastle-homes-8d23861755b7.json' # Проверьте этот путь!

# Замініть на назву вашої Google таблиці та аркуша
SPREADSHEET_NAME = 'hastlehomes2(Аркуш1).csv' # Уверены, что это имя файла, а не таблицы? Обычно указывают имя таблицы.
WORKSHEET_NAME = 'Аркуш1'

# --- Функція для збереження даних у Google Sheets ---
def save_to_google_sheets(data):
    """
    Авторизується в Google Sheets та записує дані вказаний аркуш.
    Повертає True у разі успіху, False у разі помилки.
    """
    try:
        # Проверка существования файла перед использованием
        if not os.path.exists(CREDENTIALS_FILE):
             print(f"ПОМИЛКА: Файл облікових даних не знайдено за шляхом: {CREDENTIALS_FILE}")
             return False

        creds = Credentials.from_service_account_file(CREDENTIALS_FILE, scopes=['https://www.googleapis.com/auth/spreadsheets']) # Явно укажем scopes
        gc = gspread.authorize(creds)

        # Открываем по имени ТАБЛИЦЫ, а не файла CSV
        spreadsheet = gc.open(SPREADSHEET_NAME.replace('.csv','')) # Убираем .csv, если это имя таблицы
        worksheet = spreadsheet.worksheet(WORKSHEET_NAME)

        # Логика добавления заголовков и данных (выглядит нормально)
        # ... (ваш код добавления заголовков и данных) ...
        # Вставил ваш код обратно для полноты
        existing_headers = worksheet.row_values(1) if worksheet.row_count > 0 else []
        new_headers = list(data.keys())
        headers_to_add = [header for header in new_headers if header not in existing_headers]

        # Если worksheet пуст и есть новые заголовки, записываем их
        if not existing_headers and new_headers:
             worksheet.append_row(new_headers)
             all_headers = new_headers
        # Если существующие заголовки есть, добавляем новые, если они появились
        elif headers_to_add:
             worksheet.update( [existing_headers + headers_to_add] , 'A1') # Обновляем первую строку
             all_headers = existing_headers + headers_to_add
        else:
             all_headers = existing_headers # Используем только существующие

        # Формируем строку данных в правильном порядке
        row_data = [data.get(header, '') for header in all_headers]
        worksheet.append_row(row_data) # Добавляем строку

        print("Дані успішно записано до Google таблиці!")
        return True
    except gspread.exceptions.SpreadsheetNotFound:
        print(f"ПОМИЛКА: Таблиця з назвою '{SPREADSHEET_NAME.replace('.csv','')}' не знайдена.")
        return False
    except gspread.exceptions.WorksheetNotFound:
         print(f"ПОМИЛКА: Аркуш з назвою '{WORKSHEET_NAME}' не знайдено в таблиці.")
         return False
    except Exception as e:
        print(f"Виникла помилка при записі до Google таблиці: {e}")
        return False

# --- Маршрути Flask ---
@app.route('/')
def index():
    """Віддає головну сторінку з формою."""
    # Теперь Flask будет искать index.html в папке py/templates/
    return render_template('index.html')

@app.route('/submit_form', methods=['POST'])
def submit_form():
    """
    Приймає дані з POST-запиту у форматі JSON та зберігає їх у Google Sheets.
    Повертає JSON-відповідь про успіх або помилку.
    """
    if request.method == 'POST':
        try:
            form_data = request.get_json()
            # Проверка, что данные получены и это словарь
            if not form_data or not isinstance(form_data, dict):
                 print("Помилка: Отримані некоректні дані або не JSON.")
                 return jsonify({'error': 'Некоректні дані JSON'}), 400

            print("Отримані дані форми:", form_data) # Логируем полученные данные

            if save_to_google_sheets(form_data):
                return jsonify({'message': 'Дані успішно збережено!'}), 200
            else:
                # Уточняем ошибку для клиента
                return jsonify({'error': 'Помилка при збереженні даних на сервері'}), 500
        except Exception as e:
            # Логируем общую ошибку обработки
            print(f"Помилка обробки POST-запиту /submit_form: {e}")
            return jsonify({'error': 'Внутрішня помилка сервера при обробці запиту'}), 500
    else:
        # Этот блок не должен вызываться при POST, но оставим для полноты
        return jsonify({'error': 'Дозволено лише POST-запити'}), 405

# --- Запуск Flask-додатку ---
if __name__ == '__main__':
    # Используем порт по умолчанию 5000
    app.run(host='0.0.0.0', port=5000, debug=True) # Добавлен host='0.0.0.0' для доступности извне (если нужно)
