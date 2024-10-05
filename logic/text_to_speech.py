import edge_tts as tts
import asyncio
from io import BytesIO


class TTS_Gen():
    def __init__(self, language : str, gender : str) -> None:
        self.voice = "ja-JP-NanamiNeural"

    async def __generate_mp3(self, text) -> BytesIO:
        communicate = tts.Communicate(text, self.voice)
        mp3 = BytesIO()

        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                mp3.write(chunk["data"])
        
        mp3.seek(0)
        return mp3
    
    async def text_to_mp3_batch(self, scripts : list):
        tasks = [self.__generate_mp3(script) for script in scripts]

        for task in asyncio.as_completed(tasks):  
            mp3 = await task
            yield mp3




    
    

