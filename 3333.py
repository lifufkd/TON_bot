import flet as ft
import asyncio
import requests
from pytoniq_core import Address
from connector import get_connector
from pytonconnect import TonConnect


def open_dlg(page, dlg):
    page.dialog = dlg
    dlg.open = True
    page.update()


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


async def connect_wallet(wallet_name: str, btn, balance, ton_balance, page, dlg):
    global wallet_address, link_address
    connector = get_connector(page.session_id)
    wallets_list = connector.get_wallets()
    wallet = None
    for w in wallets_list:
        if w['name'] == wallet_name:
            wallet = w

    if wallet is None:
        raise Exception(f'Unknown wallet: {wallet_name}')
    generated_url = await connector.connect(wallet)
    link_address = generated_url
    open_dlg(page, dlg)
    for i in range(1, 180):
        await asyncio.sleep(1)
        if connector.connected:
            if connector.account.address:
                btn.text = "DISCONNECT"
                tr = Address(connector.account.address).to_str(is_bounceable=False)
                wallet_address = tr
                balance.value = f'{tr[:7]}...{tr[-5:]}'
                ton_balance.value = str(get_wallet_balance(connector.account.address))
                page.update()
            return


async def disconnect_wallet(btn, balance, ton_balance, page):
    global wallet_address
    connector = get_connector(page.session_id)
    await connector.restore_connection()
    await connector.disconnect()
    btn.text = "CONNECT"
    wallet_address = 'not connected'
    balance.value = 'not connected'
    ton_balance.value = '0.0'
    page.update()


async def main_b(btn, balance, ton_balance, page, dlg):
    connector = get_connector(page.session_id)
    connected = await connector.restore_connection()
    if not connected:
        wallets_list = TonConnect.get_wallets()
        wallets = str()
        for index, wallet in enumerate(wallets_list):
            wallets += f'{index} {wallet["name"]}\n'
        await connect_wallet(wallets_list[1]["name"], btn, balance, ton_balance, page, dlg)


def main(page):
    global disconnect_button, wallet_address
    page.title = "Climbing Club"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.bgcolor = ft.colors.TRANSPARENT
    dlg = None

    def click_btn(e):
        global switch
        if not switch:
            switch = True
            asyncio.run(main_b(disconnect_button, balance, ton_balance, page, dlg))
        else:
            switch = False
            asyncio.run(disconnect_wallet(disconnect_button, balance, ton_balance, page))

    def alert_click(e):
        page.set_clipboard(link_address)
        dlg.open = False
        page.update()

    # Define styles
    text_style = ft.TextStyle(size=16, color=ft.colors.BLACK)
    large_text_style = ft.TextStyle(size=22, color=ft.colors.BLACK, weight=ft.FontWeight.BOLD)
    bold_text_style = ft.TextStyle(size=20, color=ft.colors.BLACK, weight=ft.FontWeight.BOLD)
    balance = ft.Text(value=wallet_address, style=large_text_style, selectable=True, expand=True,
                      text_align=ft.TextAlign.LEFT)
    balance_copy = ft.IconButton(icon=ft.icons.COPY, icon_color=ft.colors.BLACK,
                                 on_click=lambda e: page.set_clipboard(wallet_address))
    ton_balance = ft.Text("0.0", style=text_style, expand=True, text_align=ft.TextAlign.RIGHT)
    text_link = ft.Text(value='Подтвердите вход по ссылке', style=large_text_style, selectable=True, expand=True,
                        text_align=ft.TextAlign.LEFT)
    link_copy = ft.IconButton(icon=ft.icons.COPY, icon_color=ft.colors.BLACK,
                                 on_click=alert_click)
    disconnect_button = ft.ElevatedButton(
        text="CONNECT",
        width=250,
        bgcolor=ft.colors.WHITE10,
        color=ft.colors.BLACK,
        on_click=click_btn,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=10)
        ),
    )

    dlg = ft.AlertDialog(
        bgcolor=ft.colors.WHITE,
        title=ft.Row(
            controls=[
                text_link,
                link_copy,
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
    )

    your_wallet = ft.Text("Your wallet:", style=bold_text_style, color=ft.colors.BLACK, text_align=ft.TextAlign.LEFT)
    # Wallet section
    wallet_section = ft.Container(
        content=ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        balance,
                        balance_copy,
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,

                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.START,
        ),
        bgcolor=ft.colors.BLUE,
        padding=10,
        border_radius=10,
        width=250
    )

    # Balance section
    balance_section = ft.Container(
        content=ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Icon(ft.icons.ACCOUNT_BALANCE_WALLET, color=ft.colors.BLACK),
                        ft.Text("TON:", style=text_style),
                        ton_balance,
                    ],
                ),
                ft.Row(
                    controls=[
                        ft.Icon(ft.icons.ACCOUNT_BALANCE_WALLET, color=ft.colors.BLACK),
                        ft.Text("CLIMB:", style=text_style),
                        ft.Text("0.0", style=text_style, expand=True, text_align=ft.TextAlign.RIGHT),
                    ],
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.START,
        ),
        padding=10,
        border_radius=10,
        width=250
    )

    # Bottom navigation
    bottom_nav = ft.Container(
        bgcolor=ft.colors.GREY_200,
        opacity=0.8,
        content=
            ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.IconButton(icon=ft.icons.STAR, icon_color=ft.colors.BLACK,
                                          on_click=lambda e: print("Award clicked")),
                            ft.IconButton(icon=ft.icons.HIKING, icon_color=ft.colors.BLACK,
                                          on_click=lambda e: print("Equipment clicked")),
                            ft.IconButton(icon=ft.icons.HOME, icon_color=ft.colors.BLACK,
                                          on_click=lambda e: print("Home clicked")),
                            ft.IconButton(icon=ft.icons.LANDSCAPE, icon_color=ft.colors.BLACK,
                                          on_click=lambda e: print("Climb clicked")),
                            ft.IconButton(icon=ft.icons.ACCOUNT_BALANCE_WALLET, icon_color=ft.colors.BLACK,
                                          on_click=lambda e: print("Wallet clicked")),
                        ],
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.START,
            ),
        padding=10,
        border_radius=10,
        width=250
    )

    # Assemble the layout
    layout = ft.Column(
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        alignment=ft.MainAxisAlignment.CENTER,
        controls=[
            ft.Container(
                bgcolor=ft.colors.GREY_200,
                content=
                    ft.Column(
                        controls=[
                            your_wallet,
                            wallet_section,
                            balance_section,
                            disconnect_button
                        ],
                    )
            ),
            bottom_nav,
        ],
    )

    # Center the entire layout within the page
    centered_container = ft.Container(
        content=layout,
        alignment=ft.alignment.center,
        expand=True,
    )

    # Add centered container to the page
    background_image = ft.Image(
        src="les.jpg",
    )

    # Stack background image with the content
    stack = ft.Stack(
        controls=[
            background_image,
            centered_container
        ],
        expand=True
    )

    # Add stack to the page
    page.add(stack)


if __name__ == '__main__':
    link_address = ''
    wallet_address = 'not connected'
    disconnect_button = None
    switch = False
    ft.app(target=main, view=ft.WEB_BROWSER)
