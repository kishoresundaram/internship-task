import whisper


# Load Whisper model
model = whisper.load_model("base")


def speech_to_text(audio_file: str) -> str:

    result = model.transcribe(audio_file)

    return result["text"]