import logging
import os
from datetime import datetime
from config import Info


def setup_logger():
    """
    Настраивает и возвращает логгер для приложения.

    Создает папку 'logs' (если её нет) и настраивает логгер:
    - Запись в файл с именем в формате 'logs/{имя_ассистента}_{дата}.log'
    - Вывод логов в консоль
    - Формат записей: 'время - уровень - сообщение'

    Returns:
        logging.Logger: Настроенный объект логгера с именем из Info.NAME.
    """
    if not os.path.exists('logs'):
        os.makedirs('logs')

    log_filename = f"logs/{Info.NAME}_{datetime.now().strftime('%Y-%m-%d')}.log"

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_filename),
            logging.StreamHandler()
        ]
    )

    return logging.getLogger(Info.NAME)
