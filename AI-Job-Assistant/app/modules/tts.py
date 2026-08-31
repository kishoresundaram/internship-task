import edge_tts
import uuid
import os


async def text_to_speech(text: str) -> str:

    filename = f"speech_{uuid.uuid4().hex}.mp3"

    output_path = os.path.join(
        "data",
        filename
    )

    os.makedirs("data", exist_ok=True)

    communicate = edge_tts.Communicate(
        text,
        "en-US-AriaNeural"
    )

    await communicate.save(output_path)

    return output_path