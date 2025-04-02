import pyttsx3
from vosk import Model, KaldiRecognizer
import pyaudio
import keyboard
import json 
import requests 
import time


API_KEY = "71c312c01182a6b472f489f174d58595"
BASE_URL = "https://favqs.com/api"

current_quote = None

def get_random_quote():
    global current_quote 
    endpoint = "/qotd"
    url = BASE_URL + endpoint
    response = requests.get(url)
    if response.status_code == 200:
        current_quote = response.json()  
        return current_quote
    return None

def print_quote(quote_data):
    """Красиво вывести цитату"""
    quote = quote_data.get('quote', {})
    print(f"\nАвтор: {quote.get('author', '')}")
    print(f"Цитата: {quote.get('body', '')}")
    print(f"Теги: {', '.join(quote.get('tags', []))}")
    print(f"ID: {quote.get('id', '')}")

def phrase(quote_data):
    quote = quote_data.get('quote', {})
    phrase = f"Цитата: {quote.get('body', '')}"
    return phrase 

def author(quote_data):
    quote = quote_data.get('quote', {})
    author = f"Автор: {quote.get('author', '')}"
    return author

def get_phrase_speak(random_quote):
    text = phrase(random_quote)[7:]
    print_quote(random_quote)
    tts = pyttsx3.init()

    tts.setProperty('rate', tts.getProperty('rate') - 40)
    tts.setProperty('volume', tts.getProperty('volume') + 0.9)

    voices = tts.getProperty('voices')
    for voice in voices:
        if 'en' in voice.languages or 'eng' in voice.id.lower():
            tts.setProperty('voice', voice.id)
            break
    
    
    global is_speaking
    is_speaking = True
    
    tts.say(text)
    tts.runAndWait()
    
    
    time.sleep(0.5)
    is_speaking = False


is_speaking = False

def get_author_speak():
    global current_quote
    if current_quote is None:  # Если цитаты еще нет, получаем новую
        current_quote = get_random_quote()
    
    text = author(current_quote)  # Используем текущую цитату
    print_quote(current_quote)
    
    tts = pyttsx3.init()
    tts.setProperty('rate', tts.getProperty('rate') - 40)
    tts.setProperty('volume', tts.getProperty('volume') + 0.9)

    voices = tts.getProperty('voices')
    for voice in voices:
        if 'en' in voice.languages or 'eng' in voice.id.lower():
            tts.setProperty('voice', voice.id)
            break
    
    global is_speaking
    is_speaking = True
    
    tts.say(text)
    tts.runAndWait()
    
    time.sleep(0.5)
    is_speaking = False

def get_first_phrase_speak():
    text = "Hello! Session started. Quotes of the day"
    tts = pyttsx3.init()

    tts.setProperty('rate', tts.getProperty('rate') - 40)
    tts.setProperty('volume', tts.getProperty('volume') + 0.9)

    voices = tts.getProperty('voices')
    for voice in voices:
        if 'en' in voice.languages or 'eng' in voice.id.lower():
            tts.setProperty('voice', voice.id)
            break
    
    
    global is_speaking
    is_speaking = True
    
    tts.say(text)
    tts.runAndWait()
    
    
    time.sleep(1.5)
    is_speaking = False


is_speaking = False

def get_last_phrase_speak():
    text = 'session is over, goodbye'
    tts = pyttsx3.init()


    tts.setProperty('rate', tts.getProperty('rate') - 40)  # Скорость
    tts.setProperty('volume', tts.getProperty('volume') + 0.9)  # Громкость


    voices = tts.getProperty('voices')
    for voice in voices:
        if 'en' in voice.languages or 'eng' in voice.id.lower():
            tts.setProperty('voice', voice.id)
            break
    tts.say(text)
    tts.runAndWait()


model = Model(r"C:\Program Files\vosk-model-small-ru-0.4")
rec = KaldiRecognizer(model, 8000)

p = pyaudio.PyAudio()
stream = p.open(
    format=pyaudio.paInt16, 
    channels=1, 
    rate=8000, 
    input=True, 
    frames_per_buffer=8000
)
stream.start_stream()

start = False


if __name__ == '__main__':
    print("Здравствуйте! \n"
    "Для начала работы следует сказать 'начать' \n"
    "Для переключения на следующую цитату следует сказать 'следующая' \n"
    "Чтобы узнать автора цитаты требуется сказать 'автор' или 'чьи слова'\n"
    "Для завершения работы неоходимо сказать 'стоп' или 'конец'")
    while True:
        data = stream.read(4000, exception_on_overflow=False)
        if len(data) == 0 or keyboard.is_pressed("q"):
            break

        
        if not is_speaking and rec.AcceptWaveform(data):
            result = rec.Result()
            result_dict = json.loads(result)
            recognized_text = result_dict.get('text', '').lower()
            
            if 'начать' in recognized_text and start==False:
                start = True 
                get_first_phrase_speak()
                get_phrase_speak(get_random_quote())
            
            if 'стоп' in recognized_text or 'конец' in recognized_text:
                get_last_phrase_speak()
                break
            
            if ('следующая' in recognized_text or 'следующее' in recognized_text or 'следующий' in recognized_text) and start == True:
                get_phrase_speak(get_random_quote())
            
            if ('автор' in recognized_text or 'чьи слова' in recognized_text) and start == True:
                get_author_speak() 
            
                


    stream.stop_stream()
    stream.close()
    p.terminate()





