import flet as ft

def main(page: ft.Page):
    page.title = "Images Example"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 50
    page.update()

    img = ft.Image(
        src="C:\\Users\\joaod\\Downloads\\images.jpg",
        width=100,
        height=100,
        fit=ft.ImageFit.CONTAIN,
    )
    

    page.add(img)

    
    page.update()

ft.app(main)