#####################################
#            Created by             #
#               SBR                 #
#####################################
import time
import telebot
import asyncio
import threading
from config_parser import ConfigParser
from frontend import Bot_inline_btns
import qrcode
from pytoniq_core import Address
from pytonconnect import TonConnect
from connector import get_connector
#####################################
config_name = 'secrets.json'


async def disconnect_wallet(message, user_id):
    connector = get_connector(message.chat.id)
    await connector.restore_connection()
    await connector.disconnect()
    bot.send_message(user_id, 'Вы успешно отключили кошелек')


def checker(connector, user_id):
    for i in range(1, 180):
        time.sleep(1)
        if connector.connected:
            if connector.account.address:
                wallet_address = connector.account.address
                wallet_address = Address(wallet_address).to_str(is_bounceable=False)
                bot.send_message(user_id, f'Вы успешно подключены с адресом <code>{wallet_address}</code>, введите /start')
            return
    bot.send_message(user_id, 'Время ожидание закончилось!')


async def connect_wallet(message, wallet_name):
    buttons = Bot_inline_btns()
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    connector = get_connector(message.chat.id)
    wallets_list = connector.get_wallets()
    wallet = None
    for w in wallets_list:
        if w['name'] == wallet_name:
            wallet = w
    if wallet is None:
        raise Exception(f'Неизвестный кошелек: {wallet_name}')
    generated_url = await connector.connect(wallet)
    qr.add_data(generated_url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    bot.send_photo(photo=img.get_image(), caption='Подключение займёт до 3-х минут, когда завершите подключение нажмите на кнопку "готово"', reply_markup=buttons.connect_wallet_url(generated_url))
    threading.Thread(target=checker, args=(connector, )).start()


def main():
    @bot.message_handler(commands=['start'])
    def start_msg(message):
        name_user = message.from_user.first_name
        user_id = message.from_user.id
        buttons = Bot_inline_btns()
        connector = get_connector(user_id)
        connected = connector.restore_connection()
        if connected:
            bot.send_message(user_id, f'Приветствую {name_user}! Я тестовый бот для подключения TON Wallets. Ты уже подключил кошелёк', reply_markup=buttons.disconnect_btns())
        else:
            wallets_list = TonConnect.get_wallets()
            bot.send_message(user_id, f'Приветствую {name_user}! Я тестовый бот для подключения TON Wallets. Ты ещё не подключил кошелёк', reply_markup=buttons.wallets_btns(wallets_list))

    @bot.callback_query_handler(func=lambda call: True)
    def callback(call):
        user_id = call.message.chat.id
        buttons = Bot_inline_btns()
        message = call.message
        data = call.data
        if data == 'disconnect':
            disconnect_wallet(message, user_id)
        else:
            data = data.split(':')
            if data[0] == 'connect':
                connect_wallet(message, data[1])

    bot.polling(none_stop=True)


if __name__ == "__main__":
    config = ConfigParser(config_name)
    bot = telebot.TeleBot(config.get_config()['tg_api'])
    main()
