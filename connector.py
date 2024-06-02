from pytonconnect import TonConnect
from tc_storage import TcStorage


def get_connector(chat_id: int):
    return TonConnect("https://raw.githubusercontent.com/XaBbl4/pytonconnect/main/pytonconnect-manifest.json", storage=TcStorage(chat_id))
