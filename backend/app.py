import os
import base64
import tempfile

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from dotenv import load_dotenv

load_dotenv()

from stt import transcribe_with_language
from llm_client import generate_reply, reset_history
from tts import synthesize, voice_for_language


app = FastAPI(
    title="Smart Methods Voice Assistant API"
)


# =========================================================
# CORS
# React localhost
# =========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================================================
# HOME
# =========================================================

@app.get("/")
def home():
    return {
        "status": "Smart Methods Voice Assistant API is running"
    }


# =========================================================
# VOICE PIPELINE
# =========================================================

@app.post("/api/voice")
async def voice_assistant(
    audio: UploadFile = File(...)
):

    input_path = None
    output_path = None

    try:

        # -----------------------------------------
        # save browser recording
        # -----------------------------------------

        extension = os.path.splitext(
            audio.filename or "recording.webm"
        )[1]

        if not extension:
            extension = ".webm"

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=extension
        ) as temp_audio:

            audio_bytes = await audio.read()

            temp_audio.write(audio_bytes)

            input_path = temp_audio.name


        # -----------------------------------------
        # 1. Speech To Text
        # -----------------------------------------

        user_text, language = transcribe_with_language(
            input_path
        )

        if not user_text or not user_text.strip():

            raise HTTPException(
                status_code=400,
                detail="لم يتم التعرف على كلام واضح."
            )


        # -----------------------------------------
        # 2. AI
        # -----------------------------------------

        reply_text = generate_reply(
            user_text
        )

        if not reply_text:

            raise HTTPException(
                status_code=500,
                detail="لم يتم إنشاء رد."
            )


        # -----------------------------------------
        # 3. Text To Speech
        # -----------------------------------------

        voice = voice_for_language(
            language
        )

        output_path = synthesize(
            reply_text,
            voice=voice
        )


        # -----------------------------------------
        # Audio -> Base64
        # -----------------------------------------

        with open(output_path, "rb") as file:

            reply_audio = file.read()


        audio_base64 = base64.b64encode(
            reply_audio
        ).decode("utf-8")


        extension = os.path.splitext(
            output_path
        )[1].lower()


        if extension == ".mp3":
            mime_type = "audio/mpeg"
        else:
            mime_type = "audio/wav"


        return {

            "transcript": user_text,

            "reply": reply_text,

            "language": language,

            "audio":
                f"data:{mime_type};base64,{audio_base64}"
        }


    except HTTPException:
        raise


    except Exception as error:

        print(
            "VOICE ERROR:",
            type(error).__name__,
            str(error)
        )

        raise HTTPException(
            status_code=500,
            detail=f"{type(error).__name__}: {str(error)}"
        )


    finally:

        if input_path and os.path.exists(input_path):

            try:
                os.remove(input_path)
            except:
                pass


        if output_path and os.path.exists(output_path):

            try:
                os.remove(output_path)
            except:
                pass


# =========================================================
# CLEAR MEMORY
# =========================================================

@app.post("/api/reset")
def reset():

    reset_history()

    return {
        "success": True
    }


# =========================================================
# LOCALHOST
# =========================================================

if __name__ == "__main__":

    import uvicorn

    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000
    )