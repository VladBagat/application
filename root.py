import flet as ft
from PIL import ImageGrab, Image

class MyApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.image = None
        
    def create_controls(self):
        self.welcome_text = ft.Container(content=ft.Text(value="Japanese Text to Speech", size=32), alignment=ft.alignment.center)
        self.image = ft.Container(content=ft.Image(src='result-test.jpg'), visible=False)
        self.buttons = ft.Row(controls=[ft.ElevatedButton(text="Export clipboard", on_click=self.export_clipboard),
                                        ft.ElevatedButton(text="Play sound", on_click=self.play_sound)
                                        ],
                                        alignment=ft.MainAxisAlignment.CENTER, height=830)
        
        
        #Append all created controls
        return [self.welcome_text, self.image, self.buttons]
    
    def create_overlays(self):
        self.mp3 = ft.Container(content=ft.Audio(src='test.mp3'), visible=False)

        #Append all created overlays
        return [self.mp3]

    def play_sound(self):
        pass

    def export_clipboard(self, e):
        self.image = ImageGrab.grabclipboard()

        if self.image == None: 
            raise ValueError('Cannot read clipboard')
        if not isinstance(self.image, Image.Image):
            raise ValueError('Clipboard content is not an image')

    def load_controls(self):
        controls = self.create_controls()
        overlays = self.create_overlays()
        
        for control in controls:
            self.page.add(control)
            control.visible = True

        for overlay in overlays:
            self.page.overlay.append(overlay)
        
def window(page: ft.Page):
    app = MyApp(page)
    page.window.width = 800
    page.window.height = 600

    app.load_controls()

ft.app(target=window)