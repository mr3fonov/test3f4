import os
from dotenv import load_dotenv

# Загрузка переменных окружения из .env файла
load_dotenv()

# Получение конфигурационных данных из переменных окружения
TOKEN_TG_BOT = os.getenv('TOKEN_TG_BOT')
API_BITRIX24_HOOK = os.getenv('API_BITRIX24_HOOK')

# Проверка наличия необходимых переменных окружения
if not all([TOKEN_TG_BOT, API_BITRIX24_HOOK]):
    raise ValueError("Отсутствуют необходимые переменные окружения. Проверьте .env файл.")