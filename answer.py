from speechkit import configure_credentials, creds
from speechkit import model_repository
from config import Settings, Info
from logger import setup_logger
import time

logger = setup_logger()


def answer(answer_text, filename):
    try:
        time.sleep(0.3)  # Пауза для стабилизации аудио

        configure_credentials(
            yandex_credentials=creds.YandexCredentials(
                iam_token=Settings.IAM_TOKEN
            )
        )

        model = model_repository.synthesis_model()
        model.voice = Info.VOICE
        model.role = Info.VOICE_STYLE

        result = model.synthesize(answer_text, raw_format=False)
        result.export(filename, format='wav')

    except Exception as e:
        logger.error(f"Ошибка синтеза речи: {str(e)}")
        raise
