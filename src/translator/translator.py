class Translator:
    def __init__(self, translation_service):
        self.translation_service = translation_service

    def translate(self, text):
        # Здесь должен быть вызов к API переводчика
        translated_text = self.translation_service.translate(text, target_language='ru')
        return translated_text