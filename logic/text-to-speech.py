import edge_tts as tts
import asyncio

TEXT = "言うな!もう江戸時代じゃないのだ"
VOICE = "ja-JP-NanamiNeural"
OUTPUT_FILE = r"D:\PythonProjects\Vlad-playground\TextParser\results\test.mp3"

async def amain() -> None:
    communicate = tts.Communicate(TEXT, VOICE)
    await communicate.save(OUTPUT_FILE)

if __name__ == "__main__":
    asyncio.run(amain())
