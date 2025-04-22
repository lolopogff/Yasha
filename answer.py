from speechkit import configure_credentials, creds
from speechkit import model_repository

from config import Settings, Info


def answer(answer, filename):
    configure_credentials(
        yandex_credentials=creds.YandexCredentials(
            iam_token=f"{Settings.IAM_TOKEN}"
        )
    )

    model = model_repository.synthesis_model()

    model.voice = Info.VOICE

    result = model.synthesize(answer, raw_format=False)
    result.export(filename, format='wav')
