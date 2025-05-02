from flask import Flask, request, jsonify, render_template, session
import logging
import json
import os

# --- Налаштування логування ---
# Змінено рівень логування на WARNING для продакшн (за потреби змініть на INFO або DEBUG)
logging.basicConfig(level=logging.WARNING, format='%(asctime)s - %(levelname)s - %(module)s - %(message)s')

app = Flask(__name__,
            template_folder=os.path.join(os.path.dirname(__file__), 'templates'),
            static_folder=os.path.join(os.path.dirname(__file__), '..', 'static'))

# --- Додай секретний ключ для роботи з сесіями (зроблено раніше) ---
app.secret_key = 'a3b4c5d6e7f8g9h0i1j2k3l4m5n6o7p8q9r0s1t2u3v4w5x6y7z8'

# --- Маршрути Flask ---
@app.route('/')
def index():
    logging.info("Отримано GET-запит на /")
    return render_template('index.html')

@app.route('/submit_form', methods=['POST'])
def submit_form():
    logging.info("Отримано POST-запит на /submit_form")
    if request.method == 'POST':
        try:
            form_data = request.get_json()
            logging.info(f"Отримані дані форми: {form_data}")

            # Отримуємо поточну історію анкет з сесії або ініціалізуємо порожній список
            history = session.get('anketa_history', [])
            history.append(form_data)
            session['anketa_history'] = history
            logging.info(f"Історія анкет збережена в сесію. Поточна історія: {session.get('anketa_history')}")

            return jsonify({'message': 'Дані успішно збережено!', 'redirect': '/all_submissions'}), 200
        except Exception as e:
            logging.error(f"ПОМИЛКА при обробці POST-запиту /submit_form: {e}")
            return jsonify({'error': 'Внутрішня помилка сервера при обробці запиту'}), 400
    else:
        logging.warning("Отримано не дозволений запит (не POST) на /submit_form")
        return jsonify({'error': 'Дозволено лише POST-запити'}), 405

@app.route('/all_submissions')
def all_submissions():
    logging.info("Отримано GET-запит на /all_submissions")
    history = session.get('anketa_history')
    logging.info(f"Історія анкет, отримана з сесії для відображення на /all_submissions: {history}")
    if history:
        return render_template('all_submissions.html', history=history)
    else:
        logging.info("Історія анкет в сесії відсутня (для /all_submissions).")
        return render_template('message.html', message='Історія заповнених анкет відсутня.'), 200

if __name__ == '__main__':
    logging.info("Запуск Flask-додатку в режимі розробки (НЕ ДЛЯ ПРОДАКШН!)")
    app.run(host='0.0.0.0', port=5000, debug=True) # УВАГА: debug=True не для продакшн