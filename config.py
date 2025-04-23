class Info:
    """
    Настройка информации о роботе
    Параметры:
    - NAME (имя ассистента)
    - DESCRIPTION (описание, то что используем для инструкции модели)
    - VOICE (голос, список голосов (ru, M):
     filipp, ermil, zahar, alexander, kirill, anton, madi_ru)
    """
    NAME = "Яша"
    DESCRIPTION = f"Ты умный робот по имени {NAME}, разработанный Финансовым Университетом"
    VOICE = "kirill"


class Settings:
    """
    Хранение ключей для доступа к Yandex GPT API
    """
    FOLDER_ID = "b1gv4c52iaki869acqjb"
    API_KEY = "AQVN00Kh_26JTJUCXCJ7AMjj49QuaRrFRelpISkt"
    IAM_TOKEN = "AQVN0tNAgGOR7JkXS8s95SW2-qFUgWHVn5PEp9Jz"
