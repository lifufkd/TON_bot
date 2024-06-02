#####################################
#            Created by             #
#               SBR                 #
#####################################
from telebot import types
#####################################


class Bot_inline_btns:
    def __init__(self):
        super(Bot_inline_btns, self).__init__()
        self.__markup = types.InlineKeyboardMarkup(row_width=1)

    def disconnect_btns(self):
        disconnect = types.InlineKeyboardButton('Отключить кошелёк🛍️', callback_data='disconnect')
        self.__markup.add(disconnect)
        return self.__markup

    def wallets_btns(self, data):
        markup = types.InlineKeyboardMarkup(row_width=1)
        for i in data:
            wallet = types.InlineKeyboardButton(i['name'], callback_data=f'connect:{i["name"]}')
            markup.add(wallet)
        return markup

    def connect_wallet_url(self, url):
        disconnect = types.InlineKeyboardButton('Подключить кошелёк🛍️', url=url)
        self.__markup.add(disconnect)
        return self.__markup