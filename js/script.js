// Файл: script.js

document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM полностью загружен и разобран');

    // --- Находим основные элементы ---
    const form = document.getElementById('sell-form');
    const summaryError = document.getElementById('form-summary-error');

    // Проверяем, найдена ли форма
    if (!form) {
        console.error('КРИТИЧЕСКАЯ ОШИБКА: Форма с id="sell-form" НЕ НАЙДЕНА! Валидация не будет работать.');
        return; // Прекращаем выполнение, если формы нет
    } else {
        console.log('Форма найдена:', form);
    }

    // Проверяем, найден ли блок общей ошибки
    if (!summaryError) {
        console.warn('ВНИМАНИЕ: Блок общей ошибки с id="form-summary-error" не найден.');
    }

    // --- Находим поля ввода и их элементы ошибок ---
    const fieldsToValidate = [
        { inputId: 'name', errorId: 'name-error' },
        { inputId: 'phone', errorId: 'phone-error' },
        { inputId: 'email', errorId: 'email-error' },
        { inputId: 'address', errorId: 'address-error' }
    ];

    const inputs = [];
    const errors = [];
    let allElementsFound = true;

    fieldsToValidate.forEach(field => {
        const inputElement = document.getElementById(field.inputId);
        const errorElement = document.getElementById(field.errorId);

        if (!inputElement) {
            console.warn(`ВНИМАНИЕ: Поле ввода с id="${field.inputId}" не найдено!`);
            allElementsFound = false;
        }
        if (!errorElement) {
            console.warn(`ВНИМАНИЕ: Элемент ошибки с id="${field.errorId}" не найден!`);
            allElementsFound = false;
        }

        inputs.push(inputElement);
        errors.push(errorElement);
    });

    if (!allElementsFound) {
        console.error("ОШИБКА: Не все необходимые элементы полей ввода или сообщений об ошибках найдены. Проверьте ID в HTML.");
        // Можно добавить return; если нужно остановить скрипт
    }

    // --- Добавляем слушатель на событие отправки формы ---
    console.log('Добавляем слушатель события submit к форме...');
    form.addEventListener('submit', function(event) {
        console.log('--- Событие SUBMIT сработало! ---');

        // Предотвращаем стандартную отправку формы (ОБЯЗАТЕЛЬНО!)
        event.preventDefault();
        console.log('event.preventDefault() вызван.');

        let isFormValid = true; // Флаг валидности формы

        // --- Сброс ошибок перед новой проверкой ---
        console.log('Сбрасываем предыдущие ошибки...');
        if (summaryError) {
            summaryError.style.display = 'none'; // Скрываем общую ошибку
        }
        inputs.forEach((input, index) => {
            if (input) {
                input.classList.remove('is-invalid'); // Убираем красную рамку
            }
            if (errors[index]) {
                errors[index].style.display = 'none'; // Скрываем мелкую ошибку
            }
        });

        // --- Проверка каждого поля ---
        console.log('Начинаем проверку полей...');
        inputs.forEach((input, index) => {
            if (input && input.value.trim() === '') {
                console.log(`Поле "${input.id || 'индекс ' + index}" ПУСТОЕ!`);
                isFormValid = false; // Форма невалидна
                input.classList.add('is-invalid'); // Добавляем красную рамку
                if (errors[index]) {
                    errors[index].style.display = 'block'; // Показываем мелкую ошибку
                }
            } else if (input) {
                 console.log(`Поле "${input.id || 'индекс ' + index}" заполнено.`);
            }
        });
        console.log('Проверка полей завершена. isFormValid:', isFormValid);

        // --- Обработка результата валидации ---
        if (!isFormValid) {
            // Если форма НЕ валидна
            console.log('Форма НЕ валидна, показываем общую ошибку.');
            if (summaryError) {
                summaryError.style.display = 'block'; // Показываем общий блок ошибки
            }
        } else {
            // Если форма ВАЛИДНА
            console.log('Форма ВАЛИДНА! Выполняем действие...');
            // ЗДЕСЬ ВАШ КОД ДЛЯ ОТПРАВКИ ДАННЫХ НА СЕРВЕР
            // Например, стандартная отправка формы:
            // form.submit();

            // Или сообщение об успехе (если не нужна реальная отправка):
            // alert('Спасибо! Ваша заявка принята.');
            // form.reset(); // Очистить форму после успешной отправки
        }
        console.log('--- Обработка submit завершена ---');

    }); // Конец form.addEventListener('submit', ... )
    console.log('Слушатель submit добавлен.');


    // --- Опционально: убирать ошибку при начале ввода в поле ---
    inputs.forEach((input, index) => {
        if (input) {
            input.addEventListener('input', () => {
                // Проверяем, что элемент ошибки существует перед тем как с ним работать
                if (input.value.trim() !== '' && errors[index]) {
                    input.classList.remove('is-invalid');
                    errors[index].style.display = 'none';

                    // Логика скрытия общей ошибки (можно усложнить)
                    // if (summaryError) {
                    //     summaryError.style.display = 'none';
                    // }
                }
            });
        }
    });
    console.log('Слушатели input добавлены.');

}); // Конец document.addEventListener('DOMContentLoaded', ... )