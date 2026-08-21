"""
Smart Methods LLM module.

Uses Gemini as the main LLM and grounds company-related
answers in knowledge/smart_methods.md.
"""

import os

from dotenv import load_dotenv
from google import genai

from knowledge_base import load_knowledge


load_dotenv()


# =========================================================
# CONFIG
# =========================================================

GEMINI_API_KEY = os.getenv(
    "GEMINI_API_KEY"
)

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


# =========================================================
# SYSTEM PROMPT
# =========================================================

def _build_system_prompt() -> str:

    knowledge = load_knowledge()


    base = """
You are the official bilingual voice assistant for
Smart Methods (الأساليب الذكية).

The user interacts with you by voice.

RULES:

1. Keep replies short, natural, and suitable for speech.

2. Always answer in the same language used by the user.

3. If the user speaks Arabic, answer in Arabic.

4. If the user speaks English, answer in English.

5. Your primary purpose is to answer questions about
Smart Methods.

6. For questions about Smart Methods, including:
   - company information
   - services
   - robots
   - projects
   - training programs
   - technologies
   - contact information

use ONLY the reference information provided below.

7. If information about Smart Methods is not found in the
reference data, clearly say that you do not have enough
information.

8. Do not invent Smart Methods information.

9. Keep responses concise because they will be converted
to speech.

=== SMART METHODS REFERENCE DATA ===

"""


    if knowledge:
        return base + knowledge


    return base


SYSTEM_PROMPT = _build_system_prompt()


# =========================================================
# HISTORY
# =========================================================

_history = []


def _save_history(
    user_text: str,
    assistant_text: str
):

    _history.append(
        {
            "role": "user",
            "content": user_text
        }
    )


    _history.append(
        {
            "role": "assistant",
            "content": assistant_text
        }
    )


# =========================================================
# GENERATE REPLY
# =========================================================

def generate_reply(
    text: str
) -> str:

    if not text:
        return ""


    text = text.strip()


    if not text:
        return ""


    conversation = []


    for message in _history:

        speaker = (
            "User"
            if message["role"] == "user"
            else "Assistant"
        )


        conversation.append(
            f"{speaker}: {message['content']}"
        )


    conversation.append(
        f"User: {text}"
    )


    conversation.append(
        "Assistant:"
    )


    interaction = client.interactions.create(
        model=GEMINI_MODEL,

        system_instruction=SYSTEM_PROMPT,

        input="\n".join(
            conversation
        )
    )


    reply = interaction.output_text


    if not reply:
        raise RuntimeError(
            "Gemini returned an empty reply."
        )


    reply = reply.strip()


    _save_history(
        text,
        reply
    )


    return reply


# =========================================================
# RESET
# =========================================================

def reset_history() -> None:
    _history.clear()