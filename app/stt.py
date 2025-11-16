import os
from faster_whisper import WhisperModel
import torch

def transcribe_audio(audio_path: str):
    
    if not os.path.exists(audio_path):
        print(f"File not found: {audio_path}")
        return ""

    device = "cuda" if torch.cuda.is_available() else "cpu"
    model_size = "small"  

    print(f"Using device: {device}")
    print("Loading Faster-Whisper model...")
    model = WhisperModel(model_size, device=device, compute_type="int8")

    print(f"Transcribing: {audio_path}")
    segments, info = model.transcribe(audio_path, beam_size=1, language="hi")  

    text = " ".join([segment.text.strip() for segment in segments])
    print("Transcribed:", text)
    return text


if __name__ == "__main__":
    
    input_path = "data/input/1.mp3"  
    transcribe_audio(input_path)
