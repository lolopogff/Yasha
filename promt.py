import requests

from config import Settings, Info


def promt(message):
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
    response = requests.post(url, headers=headers, json=prompt)
    result = response.json()
    text_response = result["result"]["alternatives"][0]["message"]["text"]
    return text_response
