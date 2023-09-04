import speech_recognition as sr
from settings import bot
from io import BytesIO
import soundfile
from telebot import types
from googletrans import Translator


def handler_voice(message):
    try:
        file_info = bot.get_file(message.voice.file_id)
        file = bot.download_file(file_info.file_path)

        with open("voice_message.wav", "wb") as voice_file:
            voice_file.write(file)
        # Читаємо файл
        data, samplerate = soundfile.read('voice_message.wav')
        # Повторно зберігаємо файл з правильним підтипом
        soundfile.write('new.wav', data, samplerate, subtype='PCM_16')
        recognizer = sr.Recognizer()
        with sr.AudioFile("new.wav") as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data, language='uk-UA')

        # Send the transcribed text back to the user
        # bot.reply_to(message, f"{text}")
        keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        button1 = types.KeyboardButton("Конвертація без перекладу")
        button2 = types.KeyboardButton("Конвертація з перекладом")
        keyboard.add(button1, button2)
        sent_message = bot.send_message(message.chat.id, 'Оберіть опцію: ', reply_markup=keyboard)
        bot.register_next_step_handler(sent_message, handler_translate,text)
    except:
        pass
def handler_translate(message,text):
    if message.content_type == 'text':
        if message.text == "Конвертація без перекладу":
            bot.send_message(message.chat.id, f"{text}")
        elif message.text == "Конвертація з перекладом":
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            button1 = types.KeyboardButton("🇻🇬")
            button2 = types.KeyboardButton("🇵🇱")
            button3 = types.KeyboardButton("🇪🇸")
            markup.add(button1, button2, button3)
            sent_message = bot.send_message(message.chat.id, 
                                            "Оберіть мову на яку треба перекласти", 
                                            reply_markup=markup)
            bot.register_next_step_handler(sent_message, translate_message, text)

def translate_message(message, text):
    if message.content_type == 'text':
        result_text = None
        match message.text:
            case "🇻🇬":
                result_text = translate_text(text, "en")
            case "🇵🇱":
                result_text = translate_text(text, "pl")
            case "🇪🇸":
                result_text = translate_text(text, "es")
        if result_text:
            bot.send_message(message.chat.id, result_text)
# 🇻🇬🇵🇱🇪🇸





def translate_text(text, target_language):
    translator = Translator()
    
    try:
        translation = translator.translate(text, dest=target_language)
        translated_text = translation.text
        return translated_text
    except Exception as e:
        return str(e)