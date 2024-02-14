import requests 
from .settings import Configuration as config


class TelegramUtility:

    @staticmethod
    def send_telegram_message(message : str):
           url = f"https://api.telegram.org/bot{config.telegram_token}/sendMessage?chat_id={config.telegram_chat_id}&text={message}"
           requests.get(url)
