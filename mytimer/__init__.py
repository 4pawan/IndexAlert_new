from .smartConnect import SmartConnect
import pyotp
import datetime
import logging
from .settings import Configuration as config
from .telegram_util import TelegramUtility as tu
import azure.functions as func


def main(mytimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()

    if mytimer.past_due:
        logging.info('The timer is past due!')

    logging.info('Python timer trigger function ran at %s', utc_timestamp)
    connect = SmartConnect(config.api_key)
    totp = pyotp.TOTP(config.token).now()
    data = connect.generateSession(config.username, config.pwd, totp)
    #tu.send_telegram_message(data)
    if data['status'] == False:
        tu.send_telegram_message(data)
    else:       
        index_data = connect.getMarketData("FULL", {"NSE": ["99926000", "99926009"]})['data']['fetched']
        nifty_50 = float(index_data[0]['netChange'])
        bank_nifty = float(index_data[1]['netChange'])
        is_nifty_triggered =  nifty_50 > 100 or nifty_50 < -100
        is_bank_nifty_triggered =  bank_nifty > 300 or bank_nifty < -300
        is_condition_triggered = is_nifty_triggered or is_bank_nifty_triggered
        message = f"Welcome {nifty_50}   {bank_nifty}"
        if is_condition_triggered:
             tu.send_telegram_message(message)