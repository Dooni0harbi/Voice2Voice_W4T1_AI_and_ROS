import os
import mimetypes

from dotenv import load_dotenv
from google import genai
from google.genai import types


load_dotenv()


GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise RuntimeError(
        "GEMINI_API_KEY is missing from .env"
    )


GEMINI_MODEL = os.getenv(
    "GEMINI_MODEL",
    "gemini-3.6-flash"
)


client = genai.Client(
    api_key=GEMINI_API_KEY
)


def transcribe(audio_path: str) -> str:
    text, _ = transcribe_with_language(audio_path)
    return text


def transcribe_with_language(
    audio_path: str,
    language: str = "auto"
):

    if not audio_path:
        return "", "ar"

    if not os.path.exists(audio_path):
        raise FileNotFoundError(
            f"Audio file not found: {audio_path}"
        )


    # =====================================================
    # READ AUDIO FILE
    # =====================================================

    with open(audio_path, "rb") as audio_file:
        audio_bytes = audio_file.read()


    # =====================================================
    # DETECT MIME TYPE
    # =====================================================

    mime_type, _ = mimetypes.guess_type(
        audio_path
    )


    if not mime_type:
        mime_type = "audio/webm"


    # =====================================================
    # PROMPT
    # =====================================================

    if language == "ar":

        prompt = """
قم بتحويل التسجيل الصوتي إلى نص عربي.

أعد النتيجة بهذا الشكل فقط:

LANGUAGE: ar
TEXT: النص المنطوق
"""

    elif language == "en":

        prompt = """
Transcribe the audio into English.

Return only this format:

LANGUAGE: en
TEXT: transcription
"""

    else:

        prompt = """
Transcribe the provided audio.

Detect whether the speaker is speaking Arabic or English.

Return only this format:

LANGUAGE: ar
TEXT: transcription

or:

LANGUAGE: en
TEXT: transcription
"""


    # =====================================================
    # GEMINI
    # Audio is sent INLINE.
    # No client.files.upload().
    # =====================================================

    response = client.models.generate_content(
        model=GEMINI_MODEL,

        contents=[
            prompt,

            types.Part.from_bytes(
                data=audio_bytes,
                mime_type=mime_type
            )
        ]
    )


    if not response.text:
        raise RuntimeError(
            "Gemini returned an empty transcription."
        )


    result = response.text.strip()


    # =====================================================
    # PARSE RESPONSE
    # =====================================================

    detected_language = "ar"

    transcription_lines = []


    for line in result.splitlines():

        clean_line = line.strip()


        if clean_line.upper().startswith(
            "LANGUAGE:"
        ):

            detected_language = (
                clean_line
                .split(":", 1)[1]
                .strip()
                .lower()
            )


        elif clean_line.upper().startswith(
            "TEXT:"
        ):

            transcription_lines.append(
                clean_line
                .split(":", 1)[1]
                .strip()
            )


        elif transcription_lines:

            transcription_lines.append(
                clean_line
            )


    text = " ".join(
        transcription_lines
    ).strip()


    if not text:

        text = result


    if detected_language not in (
        "ar",
        "en"
    ):

        detected_language = "ar"


    return text, detected_language