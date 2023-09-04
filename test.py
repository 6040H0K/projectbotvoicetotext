from googletrans import Translator

def translate_text(text, target_language='en'):
    translator = Translator()
    
    try:
        translation = translator.translate(text, dest=target_language)
        translated_text = translation.text
        return translated_text
    except Exception as e:
        return str(e)


print(translate_text('Привіт я Діма. Я полюбляю програмувати'))

