import flet as ft
from PIL import ImageGrab, Image
from audioplayer import AudioPlayer
import tempfile
from logic.image_to_text import Tesseract

class MyApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.image = 'placeholder.jpg'
        self.audio_player = None
        self.active_panel = None
        self.tesseract = Tesseract()
        self.loaded_image_path = None

        
    def create_controls(self):
        #GENERAL CONTROLS
        welcome_text = ft.Container(content=ft.Text(value="Japanese Text to Speech", size=32), alignment=ft.alignment.center)
        clickable_image = ft.Container(content=ft.Stack(
        controls=[
            ft.Image(src=self.image, width=600, height=400), 
            ft.ElevatedButton(
                content=ft.Icon(ft.icons.ABC, size=0),
                on_click=self.export_clipboard, 
                style=ft.ButtonStyle(
                    bgcolor=ft.colors.TRANSPARENT,  
                    elevation=0,  
                    shape=ft.RoundedRectangleBorder(radius=0),
                    padding=0  
                ),
                width=600,  
                height=330
            ),
        ],
        
        alignment=ft.alignment.center 
    ), alignment=ft.alignment.center)
        
        buttons = ft.Row(controls=[ft.ElevatedButton(text="Export clipboard", on_click=self.export_clipboard),
                                        ft.ElevatedButton(text="Generate sound", on_click=self.initiate_player)
                                        ],
                                        alignment=ft.MainAxisAlignment.CENTER, height=100)
        
        self.audio_player = ft.Container(content=AudioPlayer(self),
                                         alignment=ft.alignment.center)

        #Append all created controls
        self.active_panel = clickable_image.content
        return [welcome_text, clickable_image, self.audio_player, buttons]
    def create_overlays(self):
        self.mp3_container = ft.Container(content=ft.Audio(src='test.mp3'), visible=False)

        #Append all created overlays
        return [self.mp3_container]

    #I explicitly hate this function. I'm sorry if anyone will need to read it    
    async def initiate_player(self, e):
        scripts = self.tesseract.text_from_image(src=self.loaded_image_path)

        self.audio_player.content.visible = True
        await self.audio_player.content.start_player(scripts=scripts)

    def export_clipboard(self, e):
        image = ImageGrab.grabclipboard()

        if image == None: 
            raise ValueError('Cannot read clipboard')
        if not isinstance(image, Image.Image):
            raise ValueError('Clipboard content is not an image')

        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as temp_file:
            image.save(temp_file, format="PNG")
            temp_file_path = temp_file.name
        
        self.active_panel.controls[0].src = f"{temp_file_path}"

        self.page.update()

        self.loaded_image_path = temp_file_path
        

    def load_controls(self):
        controls = self.create_controls()
        #overlays = self.create_overlays()
        
        for control in controls:
            self.page.controls.append(control)
            control.visible = True
        
        self.page.update()

        #for overlay in overlays:
        #    self.page.overlay.append(overlay)
        
def window(page: ft.Page):
    app = MyApp(page)
    page.window.width = 800
    page.window.height = 600

    app.load_controls()

if __name__ == "__main__":
    ft.app(target=window)