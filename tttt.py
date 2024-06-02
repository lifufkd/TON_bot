import asyncio
import requests
from pytoniq_core import Address
from connector import get_connector
from pytonconnect import TonConnect


def get_wallet_balance(wallet_address):
    """Функция для получения баланса кошелька через Toncenter API"""
    try:
        # Формируем URL для запроса
        url = f"https://toncenter.com/api/v2/getAddressInformation?address={wallet_address}"

        # Отправляем GET-запрос
        response = requests.get(url)

        # Проверяем статус-код ответа
        if response.status_code == 200:
            try:
                # Пытаемся разобрать ответ как JSON
                data = response.json()
                if 'ok' in data and data['ok']:
                    balance = int(data['result']['balance']) / 10**9  # Преобразуем баланс в TON (он возвращается в нанотон)
                    return balance
                else:
                    print("Неверный формат ответа или запрос не удался")
                    return None
            except ValueError:
                print("Ошибка при парсинге JSON-ответа")
                print("Ответ сервера:", response.text)
                return None
        else:
            print(f"Ошибка при запросе: {response.status_code}")
            return None
    except Exception as e:
        print(f"Ошибка при получении баланса: {e}")
        return None


async def connect_wallet(wallet_name: str):
    connector = get_connector(777)
    wallets_list = connector.get_wallets()
    wallet = None
    for w in wallets_list:
        if w['name'] == wallet_name:
            wallet = w

    if wallet is None:
        raise Exception(f'Unknown wallet: {wallet_name}')
    generated_url = await connector.connect(wallet)
    print(f'Подтвердите вход в течение 3 минут:\n\n{generated_url}')
    for i in range(1, 180):
        await asyncio.sleep(1)
        if connector.connected:
            if connector.account.address:
                wallet_address = connector.account.address
                balance = get_wallet_balance(wallet_address)
                wallet_address = Address(wallet_address).to_str(is_bounceable=False)
                return wallet_address, balance
            return

    print('Время истекло!')


async def disconnect_wallet():
    connector = get_connector(777)
    await connector.restore_connection()
    await connector.disconnect()
    print('Вы успешно отключили кошелёк')


async def main():
    connector = get_connector(777)
    connected = await connector.restore_connection()
    if connected:
        print('Вы уже подключены')
    else:
        wallets_list = TonConnect.get_wallets()
        wallets = str()
        for index, wallet in enumerate(wallets_list):
            wallets += f'{index} {wallet["name"]}\n'
        wallet_address, balance = await connect_wallet(wallets_list[int(input(f'Выберите мост для подключения:\n\n{wallets}'))]["name"])
        return wallet_address, balance


if '__main__' == __name__:
    wallet_address, balance = asyncio.run(main())
    print(f'Вы успешно подключены! Адрес вашего кошелька - {wallet_address}, Баланс - {balance}')