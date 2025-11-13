import json
from agent import generate_reply
from tts import text_to_speech, LAST_TTS_FILE
from memory import append_message, get_recent_context
from pathlib import Path

CLIENTS_FILE = Path("../data/clients.json")

def load_clients():
    return json.loads(CLIENTS_FILE.read_text(encoding="utf-8"))

def get_client(user_id: str):
    clients = load_clients()
    return clients.get(user_id)

def main(user_id: str, user_text: str = None):
    client = get_client(user_id)
    if not client:
        print("Unknown client:", user_id)
        return None

    if not user_text:
        user_text = "No input detected, generating greeting..."
    
    print("User:", user_text)

    context = get_recent_context(user_id)
    context_text = "\n".join([f"{m['direction']}: {m['text']}" for m in context])

    prompt = (
        f"You are Riverwood Assistant.\n"
        f"Client Name: {client['name']}\n"
        f"Location: {client['location']}\n"
        f"Context:\n{context_text}\n"
        f"User said: {user_text}"
    )
    response = generate_reply(prompt)
    reply_text = response["message"]
    print("Riverwood:", reply_text)

    audio_file = text_to_speech(reply_text, play_audio=False)
    print("Audio file generated at:", audio_file)

    append_message(user_id, "user", user_text)
    append_message(user_id, "assistant", reply_text, audio_path=audio_file)

    print("Conversation saved for user:", user_id)
    
    return audio_file
