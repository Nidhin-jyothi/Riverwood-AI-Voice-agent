import os
import requests
from dotenv import load_dotenv

load_dotenv()
ELEVEN_API_KEY = os.getenv("ELEVEN_API_KEY")
VOICE_ID = "mActWQg9kibLro6Z2ouY"

TTS_DIR = os.path.join(os.getcwd(), "data", "tts")
os.makedirs(TTS_DIR, exist_ok=True)
LAST_TTS_FILE = os.path.join(TTS_DIR, "last_tts.mp3")

def text_to_speech(text: str, play_audio: bool = True):
    if not ELEVEN_API_KEY:
        raise ValueError("ELEVEN_API_KEY not found in environment.")

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
    headers = {
        "xi-api-key": ELEVEN_API_KEY,
        "Content-Type": "application/json"
    }
    data = {
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75
        }
    }

    response = requests.post(url, headers=headers, json=data)
    if response.status_code != 200:
        raise Exception(f"TTS request failed: {response.text}")

    with open(LAST_TTS_FILE, "wb") as f:
        f.write(response.content)

    if play_audio:
        try:
            import playsound
            playsound.playsound(LAST_TTS_FILE)
        except:
            pass

    return LAST_TTS_FILE
