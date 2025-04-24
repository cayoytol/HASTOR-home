import gspread
from google.oauth2.service_account import Credentials

# Шлях до вашого JSON-файлу з обліковими даними
CREDENTIALS_FILE = '"C:\Users\zyuzk\OneDrive\Desktop\ссаный сайт\Site--\py\hastle-homes-8d23861755b7.json"'  # Замініть на фактичний шлях до файлу

# Назва вашої Google таблиці
SPREADSHEET_NAME = 'hastlehomes'  # Замініть на назву вашої Google таблиці

# Назва аркуша, куди ви хочете записувати дані
WORKSHEET_NAME = 'Аркуш1'  # Замініть на назву вашого аркуша

def save_to_google_sheets(data):
    """
    Авторизується в Google Sheets та записує дані вказаний аркуш.

    Args:
        data (dict): Словник з даними для запису. Ключі словника
                     будуть використані як заголовки стовпців (якщо їх ще немає),
                     а значення - як дані рядка.
    """
    try:
        # Створення облікових даних із файлу
        creds = Credentials.from_service_account_file(CREDENTIALS_FILE)

        # Авторизація в Google Sheets API
        gc = gspread.authorize(creds)

        # Відкриття таблиці за назвою
        spreadsheet = gc.open(SPREADSHEET_NAME)

        # Вибір потрібного аркуша
        worksheet = spreadsheet.worksheet(WORKSHEET_NAME)

        # Отримання існуючих заголовків стовпців
        existing_headers = worksheet.row_values(1) if worksheet.row_count > 0 else []

        # Отримання ключів з переданих даних
        new_headers = list(data.keys())

        # Оновлення заголовків, якщо є нові
        headers_to_add = [header for header in new_headers if header not in existing_headers]
        if headers_to_add:
            worksheet.append_row(existing_headers + headers_to_add)

        # Створення рядка даних у правильному порядку стовпців
        row_data = []
        all_headers = existing_headers + headers_to_add
        for header in all_headers:
            row_data.append(data.get(header, ''))

        # Додавання нового рядка з даними
        worksheet.append_row(row_data)
        print("Дані успішно записано до Google таблиці!")

    except Exception as e:
        print(f"Виникла помилка при записі до Google таблиці: {e}")

if __name__ == '__main__':
    # Приклад використання:
    form_data = {
        "Ім'я": "Іван",
        "Прізвище": "Петренко",
        "Електронна пошта": "ivan.petrenko@example.com",
        "Телефон": "+380123456789"
    }
    save_to_google_sheets(form_data)

    # Ви можете викликати функцію save_to_google_sheets з даними,
    # які ви отримуєте з вашої веб-форми.
