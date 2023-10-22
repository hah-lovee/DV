import os
from gtts import gTTS
import speech_recognition as sr
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from pydub import AudioSegment

bot = telebot.TeleBot('6644384647:AAHAqwZc0PCO7m7vhXO_eON_ZLtvNk4WHCo')

lang=''


def write_file(voice_to_text: str) -> None:
    with open('voice_to_text.txt', 'w', encoding='utf-8') as file:
        file.writelines(voice_to_text)

def lplus(l) -> str:
    s=l+"-"+l.upper()
    return s
def Recognition(s) -> str:
    global text
    global lang
    r=sr.Recognizer()
    with sr.AudioFile(s) as sourse:
        audio = r.record(sourse)
    try:
         text = r.recognize_google(audio,language=lang)
         write_file(text)
    except sr.UnknownValueError:
         print("Don't ubderstand audio")
    except sr.RequestError as e:
        print("Error; {0}".format(e))
    return text
def ol(S):
    if S=='Русский':
        return 'ru'
    if S=='English':
        return 'en'

@bot.message_handler(commands=['start'])
def choose_language(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton('English'))
    markup.add(KeyboardButton('Русский'))
    bot.send_message(message.chat.id, "Выберите язык:", reply_markup=markup)


@bot.message_handler(func=lambda message: message.text in ['English', 'Русский'])
def handle_language_choice(message):
    global lang
    lang=ol(message.text)
    bot.send_message(message.chat.id, f"Вы выбрали язык: {message.text}. Отправьте голосовое сообщение или аудиофайл.")


@bot.message_handler(content_types=['voice', 'audio'])
def handle_audio(message):
    global lang
    save_and_send_audio(message)

def save_and_send_audio(message):
    global lang
    file_id = message.voice.file_id if message.voice else message.audio.file_id
    file_info = bot.get_file(file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    ogg_file_name = f'{lang}_audio.ogg'
    with open(ogg_file_name, 'wb') as new_file:
        new_file.write(downloaded_file)
    wav_file_name = f'{lang}_test.wav'
    audio = AudioSegment.from_ogg(ogg_file_name)
    audio.export(wav_file_name, format="wav")
    print("Wav ready")
    gotten_text=Recognition(wav_file_name)
    print("Текст распознан: " + gotten_text)
    tts = gTTS(gotten_text, lang=lang)
    tts.save('Audio/YourAnswer.mp3')
    sendet_audio= open ("Audio/YourAnswer.mp3", 'rb')
    bot.send_audio(message.chat.id, sendet_audio)
    os.remove(ogg_file_name)
    os.remove(wav_file_name)
    os.remove("Audio/YourAnswer.mp3")
bot.polling(none_stop=True)

