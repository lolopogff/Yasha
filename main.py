import os
import random
import time
from pygame import mixer
import speech_recognition as sr
import promt
import answer
from config import Info
from logger import setup_logger
import warnings

warnings.filterwarnings("ignore", message="Couldn't find ffmpeg or avconv")
logger = setup_logger()


def listen_command():
    """
    Слушает микрофон и возвращает распознанную команду.
    Returns:
        str: Распознанная команда или сообщение об ошибке.
    Raises:
        sr.UnknownValueError: Если речь не распознана.
        sr.RequestError: Если ошибка сервиса распознавания.
    """
    r = sr.Recognizer()
    with sr.Microphone() as source:
        logger.info("Ожидание команды пользователя...")
        print("Скажите вашу команду: ")
        audio = r.listen(source)

    try:
        our_speech = r.recognize_google(audio, language='ru-RU')
        logger.info(f"Пользователь сказал: {our_speech}")
        print("Вы сказали: " + our_speech)
        return our_speech
    except sr.UnknownValueError:
        error_msg = "Ошибка распознавания речи"
        logger.error(error_msg)
        return error_msg
    except sr.RequestError:
        error_msg = "Ошибка сервиса распознавания речи"
        logger.error(error_msg)
        return error_msg


def do_this_command(message):
    """
    Выполняет команду, распознанную в listen_command().
    - Обрабатывает ключевое слово "Пока" (завершение работы программы).
        Returns:
        None
    Raises:
        None
    """
    message = message.lower()
    if message in Info.CONCLUDING_PHRASES:
        say_message("Пока! До новых встреч!")
        exit()

    result = promt.promt(message)
    say_message(result)


def say_message(message):
    """
    Сохраняет и воспроизводит аудиофайл с уникальным именем (ответ ассистента),
    затем удаляет аудиофайл.
        Returns:
        None
    Raises:
        None
    """
    filename = f"_audio_{time.time()}_{random.randint(0, 100000)}.wav"

    answer.answer(message, filename)

    mixer.init()
    mixer.music.load(filename)
    mixer.music.play()

    while mixer.music.get_busy():
        time.sleep(0.1)

    logger.info(f"Ассистент ответил: {message}")
    print(f"{Info.NAME}: " + message)
    mixer.quit()
    os.remove(filename)


if __name__ == '__main__':
    logger.info("Запуск ассистента")
    say_message("Привет! Чем могу помочь?")
    while True:
        command = listen_command()
        do_this_command(command)
