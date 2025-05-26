import requests
from typing import Dict
from config import API_BITRIX24_HOOK
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BITRIX_WEBHOOK_URL = API_BITRIX24_HOOK

def send_to_bitrix24(data: Dict[str, str]) -> bool:
    try:
        # Валидация входных данных
        required_fields = ['service', 'name', 'phone', 'age']
        if not all(field in data for field in required_fields):
            logger.error(f"Missing required fields in data: {data}")
            return False

        # Формирование данных для отправки
        payload = {
            'fields': {
                'TITLE': f"Заказ: {data['service']}",
                'NAME': data['name'],
                'PHONE': [{'VALUE': data['phone'], 'VALUE_TYPE': 'WORK'}],
                'COMMENTS': f"Заказанная услуга: {data['service']}\nВозраст клиента: {data['age']}"
            }
        }

        # Отправка данных в Bitrix24
        response = requests.post(BITRIX_WEBHOOK_URL, json=payload, timeout=10)
        response.raise_for_status()
        
        logger.info(f"Successfully sent lead to Bitrix24: {data['name']}")
        return True

    except requests.exceptions.RequestException as e:
        logger.error(f"Error sending data to Bitrix24: {e}")
        raise

    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise