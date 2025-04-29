document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM повністю завантажений і розібраний');

    // --- Находимо основні елементи ---
    const form = document.getElementById('sell-form');
    const summaryError = document.getElementById('form-summary-error');
    const successMessage = document.createElement('div'); // Создаем элемент для сообщения об успехе
    successMessage.className = 'form-success-message';
    successMessage.style.display = 'none'; // Сначала скрываем его
    form.parentNode.insertBefore(successMessage, form.nextSibling); // Добавляем после формы

    if (!form) {
        console.error('КРИТИЧЕСКАЯ ОШИБКА: Форма з id="sell-form" НЕ ЗНАЙДЕНА! Валідація не буде працювати.');
        return;
    } else {
        console.log('Форма знайдена:', form);
    }

    if (!summaryError) {
        console.warn('ВНИМАНИЕ: Блок загальної помилки з id="form-summary-error" не знайдено.');
    }

    const fieldsToValidate = [
        { inputId: 'name', errorId: 'name-error', required: true },
        { inputId: 'phone', errorId: 'phone-error', required: true },
        { inputId: 'email', errorId: 'email-error', required: false },
        { inputId: 'address', errorId: 'address-error', required: false }
    ];

    const inputs = [];
    const errors = [];
    let allElementsFound = true;

    fieldsToValidate.forEach(field => {
        const inputElement = document.getElementById(field.inputId);
        const errorElement = document.getElementById(field.errorId);

        if (!inputElement) {
            console.warn(`ВНИМАНИЕ: Поле введення з id="${field.inputId}" не знайдено!`);
            allElementsFound = false;
        }
        if (!errorElement) {
            console.warn(`ВНИМАНИЕ: Елемент помилки з id="${field.errorId}" не знайдено!`);
            allElementsFound = false;
        }

        inputs.push(inputElement);
        errors.push(errorElement);
    });

    if (!allElementsFound) {
        console.error("ОШИБКА: Не всі необхідні елементи полів введення або повідомлень про помилки знайдено. Перевірте ID в HTML.");
    }

    console.log('Додаємо слухача події submit до форми...');
    form.addEventListener('submit', function(event) {
        console.log('--- Подія SUBMIT спрацювала! ---');
        event.preventDefault();
        console.log('event.preventDefault() викликано.');

        let isFormValid = true;

        console.log('Скидаємо попередні помилки...');
        if (summaryError) {
            summaryError.style.display = 'none';
            console.log('Загальна помилка прихована.');
        }
        inputs.forEach((input, index) => {
            if (input) {
                input.classList.remove('is-invalid');
                console.log(`Поле "${input.id || 'індекс ' + index}": червона рамка прибрана.`);
            }
            if (errors[index]) {
                errors[index].style.display = 'none';
                console.log(`Помилка для поля "${inputs[index]?.id || 'індекс ' + index}": прихована.`);
            }
        });

        console.log('Починаємо перевірку полів...');
        fieldsToValidate.forEach((field, index) => {
            const input = inputs[index];
            const error = errors[index];

            if (input && field.required && input.value.trim() === '') {
                console.log(`Поле "${input.id || 'індекс ' + index}" ПУСТЕ!`);
                isFormValid = false;
                input.classList.add('is-invalid');
                console.log(`Поле "${input.id || 'індекс ' + index}": додано червону рамку.`);
                if (error) {
                    error.style.display = 'block';
                    console.log(`Помилка для поля "${input.id || 'індекс ' + index}": показана.`);
                }
            } else if (input) {
                console.log(`Поле "${input.id || 'індекс ' + index}" заповнено.`);
            }
        });
        console.log('Перевірка полів завершена. isFormValid:', isFormValid);

        if (!isFormValid) {
            console.log('Форма НЕ валідна, показуємо загальну помилку.');
            if (summaryError) {
                summaryError.style.display = 'block';
                console.log('Загальна помилка показана.');
            }
        } else {
            console.log('Форма ВАЛІДНА! Відправляємо дані на сервер...');

            const formData = new FormData(form);
            const dataToSend = {};
            formData.forEach((value, key) => {
                dataToSend[key] = value;
            });
            console.log('Дані для відправки:', dataToSend);

            console.log('Відправляємо POST-запит на /submit_form...');
            fetch('/submit_form', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(dataToSend),
            })
            .then(response => {
                console.log('Відповідь від сервера отримана:', response);
                return response.json();
            })
            .then(data => {
                console.log('Дані від сервера оброблені:', data);
                successMessage.textContent = 'Дякуємо! Вашу заявку прийнято.';
                successMessage.style.display = 'block'; // Показываем сообщение об успехе
                form.reset(); // Очищаем форму
                console.log('Форма очищена.');
            })
            .catch(error => {
                console.error('Помилка при відправці даних на сервер:', error);
                alert('Виникла помилка при відправці даних. Будь ласка, спробуйте пізніше.');
            });
        }
        console.log('--- Обробка submit завершена ---');

    });

    inputs.forEach((input, index) => {
        if (input) {
            input.addEventListener('input', () => {
                if (input.value.trim() !== '' && errors[index]) {
                    input.classList.remove('is-invalid');
                    errors[index].style.display = 'none';
                    console.log(`Поле "${input.id || 'індекс ' + index}": помилка прихована після введення.`);
                }
            });
            console.log(`Слухача input додано до поля "${input.id || 'індекс ' + index}".`);
        }
    });
    console.log('Слухачі input додані до всіх полів.');

});