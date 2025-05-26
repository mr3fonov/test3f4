from telebot import TeleBot
from typing import Dict
from bot.bitrix24 import send_to_bitrix24

class UserState:
    def __init__(self):
        self.data: Dict[int, dict] = {}
    
    def get_data(self, user_id: int) -> dict:
        if user_id not in self.data:
            self.data[user_id] = {}
        return self.data[user_id]
    
    def clear_data(self, user_id: int) -> None:
        if user_id in self.data:
            del self.data[user_id]

user_state = UserState()

def validate_age(age: str) -> bool:
    try:
        age_num = int(age)
        return 0 < age_num < 150
    except ValueError:
        return False

def validate_phone(phone: str) -> bool:
    return phone.replace('+', '').replace('-', '').isdigit()

def register_handlers(bot: TeleBot):
    @bot.message_handler(commands=['start'])
    def start(message):
        try:
            user_state.clear_data(message.chat.id)
            msg = bot.send_message(message.chat.id, "Какую услугу вы хотите заказать?")
            bot.register_next_step_handler(msg, process_service_step)
        except Exception as e:
            bot.send_message(message.chat.id, "Произошла ошибка. Пожалуйста, попробуйте снова /start")
            print(f"Error in start handler: {e}")

    def process_service_step(message):
        try:
            if not message.text or len(message.text.strip()) < 2:
                msg = bot.send_message(message.chat.id, "Пожалуйста, введите корректное название услуги")
                bot.register_next_step_handler(msg, process_service_step)
                return

            user_data = user_state.get_data(message.chat.id)
            user_data['service'] = message.text.strip()
            msg = bot.send_message(message.chat.id, "Как вас зовут?")
            bot.register_next_step_handler(msg, process_name_step)
        except Exception as e:
            bot.send_message(message.chat.id, "Произошла ошибка. Пожалуйста, попробуйте снова /start")
            print(f"Error in service step: {e}")

    def process_name_step(message):
        try:
            if not message.text or len(message.text.strip()) < 2:
                msg = bot.send_message(message.chat.id, "Пожалуйста, введите корректное имя")
                bot.register_next_step_handler(msg, process_name_step)
                return

            user_data = user_state.get_data(message.chat.id)
            user_data['name'] = message.text.strip()
            msg = bot.send_message(message.chat.id, "Сколько вам лет?")
            bot.register_next_step_handler(msg, process_age_step)
        except Exception as e:
            bot.send_message(message.chat.id, "Произошла ошибка. Пожалуйста, попробуйте снова /start")
            print(f"Error in name step: {e}")

    def process_age_step(message):
        try:
            if not validate_age(message.text.strip()):
                msg = bot.send_message(message.chat.id, "Пожалуйста, введите корректный возраст (число от 1 до 150)")
                bot.register_next_step_handler(msg, process_age_step)
                return

            user_data = user_state.get_data(message.chat.id)
            user_data['age'] = message.text.strip()
            msg = bot.send_message(message.chat.id, "Введите ваш телефон:")
            bot.register_next_step_handler(msg, process_phone_step)
        except Exception as e:
            bot.send_message(message.chat.id, "Произошла ошибка. Пожалуйста, попробуйте снова /start")
            print(f"Error in age step: {e}")

    def process_phone_step(message):
        try:
            if not validate_phone(message.text.strip()):
                msg = bot.send_message(message.chat.id, "Пожалуйста, введите корректный номер телефона")
                bot.register_next_step_handler(msg, process_phone_step)
                return

            user_data = user_state.get_data(message.chat.id)
            user_data['phone'] = message.text.strip()
            
            try:
                send_to_bitrix24(user_data)
                bot.send_message(message.chat.id, "Спасибо, ваш заказ принят!")
            except Exception as e:
                bot.send_message(message.chat.id, "Извините, произошла ошибка при обработке заказа. Пожалуйста, попробуйте позже.")
                print(f"Error sending to Bitrix24: {e}")
            finally:
                user_state.clear_data(message.chat.id)