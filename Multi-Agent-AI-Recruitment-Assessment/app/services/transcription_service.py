from pathlib import Path
from typing import Any

from faster_whisper import WhisperModel


class TranscriptionService:
    """
    Local speech-to-text service using faster-whisper.
    """

    def __init__(
        self,
        model_size: str = "base",
        device: str = "cpu",
        compute_type: str = "int8",
    ):
        self.model = WhisperModel(
            model_size,
            device=device,
            compute_type=compute_type,
        )

    def transcribe(self, file_path: str) -> dict[str, Any]:

        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(
                f"Media file not found: {file_path}"
            )

        segments, info = self.model.transcribe(
            str(path),
            beam_size=5,
            vad_filter=True,
        )

        transcript_segments = []

        for segment in segments:
            transcript_segments.append(
                {
                    "start": round(segment.start, 2),
                    "end": round(segment.end, 2),
                    "text": segment.text.strip(),
                }
            )

        transcript = " ".join(
            item["text"]
            for item in transcript_segments
        ).strip()

        return {
            "transcript": transcript,
            "segments": transcript_segments,
            "language": info.language,
            "language_probability": round(
                info.language_probability,
                4,
            ),
        }