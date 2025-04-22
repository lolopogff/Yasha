import os
import random
import time
from pygame import mixer
import speech_recognition as sr
import promt
import answer
from config import Info


def listen_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Скажите вашу команду: ")
        audio = r.listen(source)

    try:
        our_speech = r.recognize_google(audio, language='ru-RU')
        print("Вы сказали: " + our_speech)
        return our_speech
    except sr.UnknownValueError:
        return "Ошибка распознавания"
    except sr.RequestError:
        return "Ошибка сервиса"


def do_this_command(message):
    message = message.lower()
    if message == "пока":
        say_message("Пока! До новых встреч!")
        exit()

    result = promt.promt(message)
    say_message(result)


def say_message(message):
    filename = f"_audio_{time.time()}_{random.randint(0, 100000)}.wav"

    answer.answer(message, filename)

    mixer.init()
    mixer.music.load(filename)
    mixer.music.play()

    while mixer.music.get_busy():
        time.sleep(0.1)

    print(f"{Info.NAME}: " + message)
    mixer.quit()
    os.remove(filename)


if __name__ == '__main__':
    say_message("Привет! Чем могу помочь?")
    while True:
        command = listen_command()
        do_this_command(command)


# логирование, стандартные фразы(если нету интерната)