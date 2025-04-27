import tkinter as tk
from deep_translator import GoogleTranslator
import pytesseract
from PIL import ImageGrab
import keyboard  # Для отслеживания нажатий клавиш
import pyautogui  # Для получения координат мыши
import re  # Для очистки текста

# Укажите путь к tesseract.exe
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Глобальная переменная для хранения координат точек
points = []
current_page = 0  # Текущая страница

def translate_text(text, target_language="ru"):
    """Перевод текста с помощью Google Translator."""
    if len(text.strip()) < 2:
        return text  # Возвращаем текст без перевода
    try:
        print(f"Текст для перевода: {text}")  # Отладочный вывод
        translator = GoogleTranslator(source="en", target=target_language)
        return translator.translate(text)
    except Exception as e:
        print(f"Ошибка перевода: {e}")
        return "Ошибка перевода"

def clean_text(text):
    """Очищает текст от лишних символов и исправляет ошибки OCR."""
    # Убираем лишние символы, оставляем только буквы, цифры и базовые знаки препинания
    text = re.sub(r"[^\w\s.,!?\"'()-]", "", text)
    # Убираем лишние пробелы
    text = re.sub(r"\s+", " ", text).strip()
    # Убираем пустые скобки
    text = re.sub(r"\(\s*\)", "", text)
    # Убираем лишние открытые и закрытые скобки
    text = re.sub(r"\(\s*", "(", text)
    text = re.sub(r"\s*\)", ")", text)
    # Убираем скобки, если они не содержат текста внутри
    text = re.sub(r"\([^a-zA-Z0-9\s]*\)", "", text)
    # Убираем лишние точки или запятые в начале и конце текста
    text = re.sub(r"^[.,!?]+", "", text)
    text = re.sub(r"[.,!?]+$", "", text)
    return text

def capture_text_from_book(book_bbox):
    """Захватывает текст из указанной области книги."""
    screenshot = ImageGrab.grab(book_bbox)
    # Используем дополнительные параметры для улучшения OCR
    custom_config = r'--oem 3 --psm 6'
    text = pytesseract.image_to_string(screenshot, lang="eng", config=custom_config)
    print(f"Распознанный текст: {text}")  # Отладочный вывод
    cleaned_text = clean_text(text)
    print(f"Очищенный текст: {cleaned_text}")  # Отладочный вывод
    return cleaned_text

def wait_for_points():
    """Ожидает, пока пользователь укажет 4 точки."""
    print("Нажмите клавишу (апостроф) для указания 4 точек границ книги.")
    while len(points) < 4:
        if keyboard.is_pressed(40):  # Используем скан-код клавиши апострофа
            # Получаем текущие координаты курсора
            x, y = pyautogui.position()
            points.append((x, y))
            print(f"Точка {len(points)}: {points[-1]}")
            keyboard.wait(40)  # Ждём отпускания клавиши
    print("Все точки указаны:", points)

def display_translation():
    """Отображает перевод текста рядом с книгой."""
    global current_page

    # Ожидаем указания точек
    wait_for_points()

    # Определяем границы книги
    x1, y1 = points[0]
    x2, y2 = points[2]
    book_bbox = (x1, y1, x2, y2)

    # Создание окна для перевода
    root = tk.Tk()
    root.overrideredirect(True)  # Убираем рамки окна
    root.attributes("-topmost", True)  # Поверх всех окон
    root.attributes("-transparentcolor", "black")  # Прозрачный фон

    # Установка размера окна для перевода (рядом с книгой)
    translation_width = 300  # Ширина окна перевода
    translation_height = y2 - y1  # Высота окна перевода
    translation_x = x2 + 20  # Расположение окна справа от книги
    translation_y = y1

    root.geometry(f"{translation_width}x{translation_height + 50}+{translation_x}+{translation_y}")
    root.configure(bg="black")  # Прозрачный фон

    canvas = tk.Canvas(root, bg="black", highlightthickness=0)
    canvas.pack(fill=tk.BOTH, expand=True)

    # Добавление текста перевода
    text_id = canvas.create_text(
        10,  # Отступ слева
        10,  # Отступ сверху
        text="",
        font=("Arial", 16),
        fill="white",  # Цвет текста
        anchor="nw",  # Привязка текста к верхнему левому углу
        width=translation_width - 20  # Учитываем отступы
    )

    def update_translation():
        """Обновляет перевод текста."""
        global current_page

        # Захват текста из книги
        english_text = capture_text_from_book(book_bbox)
        if not english_text.strip():
            canvas.itemconfig(text_id, text="Текст не найден.")
            root.after(1000, update_translation)
            return

        print(f"Распознанный текст (страница {current_page}): {english_text}")

        # Перевод текста
        translated_text = translate_text(english_text)
        print(f"Переведённый текст: {translated_text}")

        # Обновление текста в окне
        canvas.itemconfig(text_id, text=translated_text)

        # Автоматическое обновление через 2 секунды
        root.after(2000, update_translation)

    def exit_program():
        """Закрывает программу."""
        root.destroy()

    # Добавление кнопки выхода
    exit_button = tk.Button(root, text="Выход", command=exit_program, bg="red", fg="white")
    exit_button.pack(side=tk.BOTTOM, pady=5)

    update_translation()
    root.mainloop()

def main():
    print("Запуск переводчика Minecraft...")
    display_translation()

if __name__ == "__main__":
    main()