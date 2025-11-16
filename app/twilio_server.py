import os
from twilio.rest import Client as TwilioClient
from twilio.twiml.voice_response import VoiceResponse, Gather
from flask import Flask, request, Response, send_file
from main import main
from tts import LAST_TTS_FILE

TWILIO_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE = os.getenv("TWILIO_PHONE")
PUBLIC_URL = os.getenv("PUBLIC_URL")

twilio_client = TwilioClient(TWILIO_SID, TWILIO_TOKEN)
app = Flask(__name__)

@app.route("/audio/<audio_id>.mp3")
def serve_audio(audio_id):
    if not os.path.exists(LAST_TTS_FILE):
        return "TTS file not ready", 503
    return send_file(LAST_TTS_FILE, mimetype="audio/mpeg")

@app.route("/voice", methods=["POST"])
def voice_webhook():
    user_id = "9061061257"

    # Get user speech
    user_text = request.values.get("SpeechResult", "").strip()
    print("User said:", user_text if user_text else "[no speech detected]")

    vr = VoiceResponse()

    if user_text:
        main(user_id, user_text=user_text)
        
        gather = Gather(
            input="speech",
            timeout=20,
            speechTimeout="auto",
            action="/voice",
            method="POST",
            language="hi-IN"
        )
        gather.play(f"{PUBLIC_URL}/audio/1.mp3")
        vr.append(gather)
    else:
       
        gather = Gather(
            input="speech",
            timeout=20,
            speechTimeout="auto",
            action="/voice",
            method="POST",
            language="hi-IN"
        )
        vr.append(gather)
       
    vr.redirect("/voice")

    return Response(str(vr), mimetype="text/xml")


def initiate_call(user_id):
    user = {"phone": "+919061061257"}
    call = twilio_client.calls.create(
        to=user["phone"],
        from_=TWILIO_PHONE,
        url=f"{PUBLIC_URL}/voice"
    )
    print("Call initiated:", call.sid)


if __name__ == "__main__":
    from threading import Thread
    from time import sleep

    def start_flask():
        app.run(port=5000, debug=True, use_reloader=False)

    flask_thread = Thread(target=start_flask)
    flask_thread.start()
    sleep(5)
    initiate_call("9061061257")
    flask_thread.join()
