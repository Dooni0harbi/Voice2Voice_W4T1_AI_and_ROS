import os
import wave
import base64
import tempfile

from dotenv import load_dotenv
from google import genai


load_dotenv()


GEMINI_API_KEY = os.getenv(
    "GEMINI_API_KEY"
)

if not GEMINI_API_KEY:
    raise RuntimeError(
        "GEMINI_API_KEY is missing from .env"
    )


GEMINI_TTS_MODEL = os.getenv(
    "GEMINI_TTS_MODEL",
    "gemini-3.1-flash-tts-preview"
)


GEMINI_VOICE = os.getenv(
    "GEMINI_VOICE",
    "Kore"
)


client = genai.Client(
    api_key=GEMINI_API_KEY
)


def voice_for_language(
    language: str
) -> str:

    return GEMINI_VOICE


def synthesize(
    text: str,
    voice: str = None
) -> str:

    if not text or not text.strip():

        raise ValueError(
            "TTS text is empty"
        )


    selected_voice = (
        voice or GEMINI_VOICE
    )


    interaction = client.interactions.create(
        model=GEMINI_TTS_MODEL,

        input=text,

        response_format={
            "type": "audio"
        },

        generation_config={
            "speech_config": [
                {
                    "voice":
                        selected_voice
                }
            ]
        }
    )


    if not interaction.output_audio:

        raise RuntimeError(
            "Gemini TTS returned no audio."
        )


    audio_data = base64.b64decode(
        interaction.output_audio.data
    )


    output_path = (
        tempfile.NamedTemporaryFile(
            suffix=".wav",
            delete=False
        ).name
    )


    with wave.open(
        output_path,
        "wb"
    ) as wav_file:

        wav_file.setnchannels(1)

        wav_file.setsampwidth(2)

        wav_file.setframerate(24000)

        wav_file.writeframes(
            audio_data
        )


    return output_path