import flet as ft


def main(page):
    page.title = "Climbing Club"
    page.window_width = 300
    page.window_height = 500
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    # Set the background image
    bg_image = ft.Image(src="F:/Users/SBR/Downloads/111.jpg", fit=ft.ImageFit.COVER, height=400, width=300)

    # Wallet section
    wallet_section = ft.Column(
        controls=[
            ft.Text("Your wallet:", size=20, weight=ft.FontWeight.BOLD),
            ft.Row(
                controls=[
                    ft.Text("UQDFaxQ...f6Bxm", size=16, selectable=True),
                    ft.IconButton(icon=ft.icons.COPY, on_click=lambda e: page.set_clipboard("UQDFaxQ...f6Bxm")),
                ],
            ),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    # Balance section
    balance_section = ft.Column(
        controls=[
            ft.Row(
                controls=[
                    ft.Icon(ft.icons.ACCOUNT_BALANCE_WALLET),
                    ft.Text("TON: 0.0", size=16),
                ],
                alignment=ft.alignment.center
            ),
            ft.Row(
                controls=[
                    ft.Icon(ft.icons.ACCOUNT_BALANCE_WALLET),
                    ft.Text("CLIMB: 0.0", size=16),
                ],
                alignment=ft.alignment.center
            ),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    # Disconnect button
    disconnect_button = ft.ElevatedButton(text="DISCONNECT", on_click=lambda e: print("Disconnect clicked"))

    # Bottom navigation
    bottom_nav = ft.Row(
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        vertical_alignment=ft.CrossAxisAlignment.START,
        controls=[
            ft.IconButton(icon=ft.icons.STAR, on_click=lambda e: print("Award clicked")),
            ft.IconButton(icon=ft.icons.HIKING, on_click=lambda e: print("Equipment clicked")),  # Replaced with HIKING
            ft.IconButton(icon=ft.icons.HOME, on_click=lambda e: print("Home clicked")),
            ft.IconButton(icon=ft.icons.LANDSCAPE, on_click=lambda e: print("Climb clicked")),
            # Replaced with LANDSCAPE
            ft.IconButton(icon=ft.icons.ACCOUNT_BALANCE_WALLET, on_click=lambda e: print("Wallet clicked")),
        ],
    )

    # Assemble the layout
    layout = ft.Column(
        width=300,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        alignment=ft.MainAxisAlignment.CENTER,
        controls=[
            wallet_section,
            balance_section,
            disconnect_button,
            bottom_nav
        ],
    )

    # Center the entire layout within the page
    centered_container = ft.Container(
        content=layout,
        alignment=ft.alignment.center,
        expand=True
    )

    # Add background image and centered container to the page
    page.add(ft.Stack(controls=[bg_image, centered_container]))


# Run the app
ft.app(target=main)
