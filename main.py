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


def listen_command(timeout=None):
    """
    Слушает микрофон с возможностью таймаута.
    """
    r = sr.Recognizer()
    with sr.Microphone() as source:
        logger.info("Ожидание команды пользователя...")
        print("Скажите вашу команду: ")
        try:
            audio = r.listen(source, timeout=timeout)
            our_speech = r.recognize_google(audio, language='ru-RU')
            logger.info(f"Пользователь сказал: {our_speech}")
            print("Вы сказали: " + our_speech)
            return our_speech
        except sr.WaitTimeoutError:
            return None
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
    Сохраняет и воспроизводит аудиофайл с распознаванием стоп-слов.
    """
    filename = f"_audio_{time.time()}_{random.randint(0, 100000)}.wav"
    answer.answer(message, filename)

    mixer.init()
    mixer.music.load(filename)
    mixer.music.play()

    interrupted = False
    r = sr.Recognizer()

    def listen_for_stop():
        nonlocal interrupted
        with sr.Microphone() as source:
            r.pause_threshold = 0.8  # Увеличиваем паузу перед завершением фразы
            r.energy_threshold = 4000  # Порог чувствительности к громкости (экспериментально)
            r.dynamic_energy_threshold = False  # Фиксируем порог

            try:
                # Увеличиваем время прослушивания и снижаем фоновый шум
                print("Ожидание стоп-слова...")
                audio = r.listen(source, timeout=3, phrase_time_limit=2)
                speech = r.recognize_google(audio, language='ru-RU').lower()
                logger.debug(f"Распознано: {speech}")

                if any(stop_word in speech for stop_word in Info.STOP_PHRASES):
                    logger.info("Обнаружено стоп-слово!")
                    interrupted = True
                    mixer.music.stop()
            except sr.WaitTimeoutError:
                pass
            except Exception as e:
                logger.error(f"Ошибка при прослушивании: {str(e)}")

    # Проверяем стоп-слова чаще и с перезапуском прослушивания
    while mixer.music.get_busy() and not interrupted:
        listen_for_stop()
        time.sleep(0.1)  # Короткая пауза между проверками

    logger.info(f"Ассистент ответил: {message}")
    print(f"{Info.NAME}: {message}")

    mixer.quit()
    os.remove(filename)

    if interrupted:
        print("Воспроизведение прервано. Готов к новой команде...")


if __name__ == '__main__':
    logger.info("Запуск ассистента")
    say_message("Привет! Чем могу помочь?")
    while True:
        command = listen_command()
        do_this_command(command)
