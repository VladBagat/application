import flet as ft
from logic.text_to_speech import TTS_Gen
import tempfile

class AudioPlayer(ft.Container):
    def __init__(self, root_class):
        super().__init__()
        self.state = ""
        self.width = 350
        self.bgcolor = ft.colors.WHITE10
        self.border_radius = ft.border_radius.all(20)
        self.current_index = 0
        self.alignment = ft.alignment.center
        self.page = root_class.page
        self.tts_gen = TTS_Gen('foo', 'foo')
        self.visible = False

        self.content = ft.Column(
            controls=[
                ft.Row(
                    controls=[ft.Text(value="0/0")],
                    alignment=ft.MainAxisAlignment.CENTER
                ),
                ft.Row(
                    controls=[
                        ft.IconButton(icon=ft.icons.FAST_REWIND_ROUNDED, icon_size=20, on_click=self.fast_rewind),
                        ft.IconButton(icon=ft.icons.PLAY_CIRCLE, icon_size=25, on_click=self.play_track),
                        ft.IconButton(icon=ft.icons.FAST_FORWARD_ROUNDED, icon_size=20, on_click=self.fast_forward),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )

    def play_track(self, e):
            if self.state == "":
                self.state = "playing"
                self.content.controls[1].controls[1].icon = ft.icons.PAUSE_CIRCLE  # Access button from audio_player
                self.page.overlay[self.current_index].play()
            elif self.state == "playing":
                self.state = "paused"
                self.content.controls[1].controls[1].icon = ft.icons.PLAY_CIRCLE
                self.page.overlay[self.current_index].pause()
            else:  # if state=="paused"
                self.state = "playing"
                self.content.controls[1].controls[1].icon = ft.icons.PAUSE_CIRCLE
                self.page.overlay[self.current_index].resume()
            self.page.update()
    
    def audio_state_handler(self, e=None, action=None):
        #Manual Handling
        if not e:
            if self.state == "":
                self.content.controls[1].controls[1].icon = ft.icons.PLAY_CIRCLE
                try:
                    self.page.overlay[self.current_index].pause()
                except:
                    pass

        #Onclick handling
        else:
            # When audio ends, button goes back to null state
            if e.state == ft.AudioState.COMPLETED:
                self.state = ""
                self.content.controls[1].controls[1].icon = ft.icons.PLAY_CIRCLE

        if action == 'shift':
            self.modify_label()
         
        self.page.update()

    def modify_label(self):

        num_of_mp3 = len(self.page.overlay)
        current_mp3 = self.current_index

        label = [str(current_mp3+1), str(num_of_mp3)]

        label = '/'.join(label)
        
        self.content.controls[0].controls[0].value = str(label)

        self.page.update()

    async def start_player(self, e = None, scripts = None):
        audio_players = []

        self.page.overlay.clear()

        async for mp3 in self.tts_gen.text_to_mp3_batch(scripts=scripts):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
                temp_file.write(mp3.getvalue())

            audio_player = ft.Audio(src=str(temp_file.name), autoplay=False, on_state_changed=self.audio_state_handler)

            audio_players.append(audio_player)         

        self.page.overlay.extend(audio_players)
        self.current_index = 0
        self.page.update()   
        self.modify_label()   

    def fast_forward(self, e):
        #Ensures correct state
        self.state = ""

        self.current_index = (self.current_index + 1) % len(self.page.overlay)

        self.audio_state_handler(action='shift')
        self.page.update()


    def fast_rewind(self, e):
        #Ensures correct state
        self.state = ""
        
        self.current_index = (self.current_index - 1) % len(self.page.overlay)

        self.audio_state_handler(action='shift')
        self.page.update()