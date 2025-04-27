from flask import Flask, request, jsonify, render_template
from google.oauth2.service_account import Credentials
import gspread
import json
import os

app = Flask(__name__, template_folder='.') # Вказуємо поточну директорію як папку з шаблонами

# --- Налаштування ---
# Переконайтеся, що шлях до файлу з обліковими даними правильний
CREDENTIALS_FILE = 'C:/Users/zyuzk/OneDrive/Desktop/ссаный сайт/Site--/py/hastle-homes-8d23861755b7.json'

# Замініть на назву вашої Google таблиці та аркуша
SPREADSHEET_NAME = 'hastlehomes2(Аркуш1).csv'
WORKSHEET_NAME = 'Аркуш1'

# --- Функція для збереження даних у Google Sheets ---
def save_to_google_sheets(data):
    """
    Авторизується в Google Sheets та записує дані вказаний аркуш.
    Повертає True у разі успіху, False у разі помилки.
    """
    try:
        creds = Credentials.from_service_account_file(CREDENTIALS_FILE)
        gc = gspread.authorize(creds)
        spreadsheet = gc.open(SPREADSHEET_NAME)
        worksheet = spreadsheet.worksheet(WORKSHEET_NAME)

        existing_headers = worksheet.row_values(1) if worksheet.row_count > 0 else []
        new_headers = list(data.keys())
        headers_to_add = [header for header in new_headers if header not in existing_headers]

        if headers_to_add:
            worksheet.append_row(existing_headers + headers_to_add)

        row_data = []
        all_headers = existing_headers + headers_to_add
        for header in all_headers:
            row_data.append(data.get(header, ''))

        worksheet.append_row(row_data)
        print("Дані успішно записано до Google таблиці!")
        return True
    except Exception as e:
        print(f"Виникла помилка при записі до Google таблиці: {e}")
        return False

# --- Маршрути Flask ---
@app.route('/')
def index():
    """Віддає головну сторінку з формою."""
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
            print("Отримані дані форми:", form_data)
            if save_to_google_sheets(form_data):
                return jsonify({'message': 'Дані успішно збережено!'}), 200
            else:
                return jsonify({'error': 'Не вдалося зберегти дані до Google таблиці'}), 500
        except Exception as e:
            print(f"Помилка обробки POST-запиту: {e}")
            return jsonify({'error': 'Некоректні дані або помилка на сервері'}), 400
    else:
        return jsonify({'error': 'Дозволено лише POST-запити'}), 405

# --- Запуск Flask-додатку ---
if __name__ == '__main__':
    app.run(debug=True)