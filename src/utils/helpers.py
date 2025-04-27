def clean_text(text):
    """Удаляет лишние пробелы и символы из текста."""
    return ' '.join(text.split())

def is_english(text):
    """Проверяет, написан ли текст на английском языке."""
    return all(ord(char) < 128 for char in text)

def format_translation(original, translated):
    """Форматирует перевод для отображения."""
    return f"Перевод: {translated} (оригинал: {original})"