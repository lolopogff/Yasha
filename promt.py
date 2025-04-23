import requests
from config import Settings, Info
from logger import setup_logger

logger = setup_logger()


def promt(message):
    """
    Отправляет запрос к Yandex GPT API и возвращает очищенный ответ.

    Формирует структурированный запрос к Yandex GPT API, отправляет его, обрабатывает ответ
    и возвращает очищенный от специальных символов текст.

    Args:
        message (str): Текст сообщения пользователя, которое будет отправлено в API.

    Returns:
        str: Очищенный ответ от Yandex GPT или сообщение об ошибке в случае неудачи.

    Raises:
        Exception: Логирует ошибки, связанные с запросом к API, но не пробрасывает их выше,
                  вместо этого возвращает строку с описанием ошибки.
    """
    prompt = {
        "modelUri": f"gpt://{Settings.FOLDER_ID}/yandexgpt-lite",
        "completionOptions": {
            "stream": False,
            "temperature": 0.6,
            "maxTokens": "2000"
        },
        "messages": [
            {
                "role": "system",
                "text": f"{Info.DESCRIPTION}"
            },
            {
                "role": "user",
                "text": f"{message}"
            }
        ]
    }

    url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Api-Key {Settings.API_KEY}"
    }

    try:
        logger.info(f"Отправка запроса к Yandex GPT: {message}")
        response = requests.post(url, headers=headers, json=prompt)
        response.raise_for_status()

        result = response.json()
        text_response = result["result"]["alternatives"][0]["message"]["text"]
        cleaned_response = text_response.replace('*', '').replace('-', '')

        logger.info(f"Получен ответ от Yandex GPT: {cleaned_response}")
        return cleaned_response

    except Exception as e:
        error_msg = f"Ошибка при запросе к Yandex GPT: {str(e)}"
        logger.error(error_msg)
        return error_msg
