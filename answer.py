from speechkit import configure_credentials, creds
from speechkit import model_repository
from config import Settings, Info
from logger import setup_logger

logger = setup_logger()


def answer(answer_text, filename):
    """Синтезирует речь из текста и сохраняет результат в аудиофайл.
    Args:
        answer_text (str): Текст для синтеза речи. Должен быть не пустым и содержать
                          хотя бы несколько слов для корректной работы API.
        filename (str): Путь для сохранения результирующего аудиофайла в формате WAV.
                       Рекомендуется использовать расширение .wav
    Returns:
        None
    Raises:
        CredentialsError: Если возникла проблема с аутентификационными данными.
        SynthesisError: Если произошла ошибка во время синтеза речи.
        IOError: Если возникла проблема при сохранении файла.
        Exception: Любые другие неожиданные ошибки логируются и пробрасываются дальше.
    """
    try:
        logger.info(f"Синтез речи для текста: {answer_text}")

        configure_credentials(
            yandex_credentials=creds.YandexCredentials(
                iam_token=f"{Settings.IAM_TOKEN}"
            )
        )

        model = model_repository.synthesis_model()
        model.voice = Info.VOICE

        result = model.synthesize(answer_text, raw_format=False)
        result.export(filename, format='wav')

        logger.info(f"Аудиофайл сохранен как: {filename}")

    except Exception as e:
        error_msg = f"Ошибка при синтезе речи: {str(e)}"
        logger.error(error_msg)
        raise
