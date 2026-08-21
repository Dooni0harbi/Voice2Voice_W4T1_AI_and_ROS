# 🎙️ Smart Methods Voice-to-Voice AI Assistant

A bilingual Arabic/English **Voice-to-Voice AI Assistant** developed as part of a robotics and artificial intelligence training task.

The assistant allows the user to speak directly through the browser, converts speech into text, processes the request using an AI model, and converts the generated response back into speech.

The assistant is mainly designed to answer questions related to **Smart Methods – الأساليب الذكية** using a local company knowledge source.

---

## 🎯 Task Objective

The task required building a complete **Voice-to-Voice AI Assistant** using three main stages:

1. **Speech-to-Text**
2. **LLM Processing**
3. **Text-to-Speech**

The task also provided several tools and learning resources such as:

- Whisper
- RealtimeSTT
- OpenAI API
- Cohere
- LangChain
- RealtimeTTS

These tools were provided as implementation references and options.

In my final implementation, I followed the same required workflow using **Google Gemini-based services**.

```text
User Voice
    ↓
Speech-to-Text
    ↓
LLM Processing
    ↓
Text-to-Speech
    ↓
Voice Response
```

---

# ✅ Task Requirements & My Implementation

## 1️⃣ Speech-to-Text

### Task Requirement

Convert the user's audio input into written text.

### Suggested Resources

- Whisper
- RealtimeSTT

### My Implementation

I used **Google Gemini audio understanding** for the Speech-to-Text stage.

The user's voice is recorded directly from the browser using the **MediaRecorder API**.

The recorded audio is then sent from the React frontend to the FastAPI backend.

Gemini:

- Converts the speech into text
- Detects whether the user is speaking Arabic or English
- Returns the transcription to the backend

This fulfills the required **Speech-to-Text** stage while using Gemini instead of Whisper or RealtimeSTT.

---

## 2️⃣ LLM Processing

### Task Requirement

Send the transcribed text to a Large Language Model and generate an appropriate response.

### Suggested Resources

- OpenAI API
- Cohere
- LangChain

### My Implementation

I selected:

```text
Gemini 3.6 Flash
```

as the main Large Language Model.

The transcribed text is sent to Gemini through the FastAPI backend.

The assistant generates a short conversational response suitable for voice interaction.

The assistant also responds in the same language used by the user:

```text
Arabic Input  → Arabic Response
English Input → English Response
```

---

## 3️⃣ Text-to-Speech

### Task Requirement

Convert the generated textual response back into audio.

### Suggested Resources

- RealtimeTTS
- Python Text-to-Speech libraries

### My Implementation

I used **Gemini Text-to-Speech**.

The TTS model used in the project is:

```text
Gemini 3.1 Flash TTS Preview
```

The selected voice is:

```text
Kore
```

The generated audio is returned from the FastAPI backend to the React frontend and played automatically.

This completes the required Voice-to-Voice pipeline.

---

# 🧠 Smart Methods Knowledge Base

The main purpose of the assistant is to answer questions related to **Smart Methods – الأساليب الذكية**.

Company information is stored locally inside:

```text
backend/knowledge/smart_methods.md
```

The knowledge file is loaded through:

```text
knowledge_base.py
```

and supplied to the AI model as internal reference context.

---

## 📚 Knowledge Source

The Smart Methods information used by the assistant was collected from the company's official website and stored locally inside the project.

The assistant can use this information to answer questions related to:

- Company information
- Services
- Robots
- Projects
- Technologies
- Training programs
- Contact information

---

## 🔐 Closed-Domain Company Chatbot

For Smart Methods-related questions, the assistant behaves as a **closed-domain chatbot**.

This means that company-related answers are based on the internal Smart Methods knowledge source.

If the requested information is not available in the local knowledge source, the assistant is instructed not to invent company information.

This helps reduce hallucinations and keeps the responses grounded in the provided source.

---

## 🔎 RAG-Lite Approach

The project uses a lightweight form of **Retrieval-Augmented Generation**, referred to here as **RAG-lite**.

Instead of using:

- Vector databases
- Embeddings
- Semantic search engines

the Smart Methods knowledge file is loaded directly and included in the model context.

This approach is suitable because the company knowledge source is relatively small.

---

# 🏗️ Project Development

The project originally started with a simpler implementation using:

- Python
- Gradio
- CSS

The first version was functional, but I was not satisfied with the flexibility and visual organization of the interface.

I therefore redesigned the frontend using:

- React
- Vite
- Tailwind CSS

The project was then divided into separate **Frontend** and **Backend** sections.

```text
SmartMethods_Voice_Assistant/
│
├── backend/
│   ├── app.py
│   ├── stt.py
│   ├── tts.py
│   ├── llm_client.py
│   ├── knowledge_base.py
│   ├── requirements.txt
│   │
│   └── knowledge/
│       └── smart_methods.md
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── index.css
│   │
│   ├── public/
│   ├── package.json
│   ├── package-lock.json
│   ├── vite.config.js
│   ├── eslint.config.js
│   └── index.html
│
├── assets/
│   ├── voice-to-voice-demo.mov
│   ├── frontend.png
│   ├── sending_request.png
│   ├── arabic_result.png
│   └── english_result.png
│
├── .gitignore
├── .env.example
└── README.md
```

This separation improved project organization and gave me more control over the user interface.

---

# 🎨 Frontend Design

The frontend was built using:

```text
React + Vite + Tailwind CSS
```

The interface includes:

- Smart Methods-inspired colors
- Gradient background
- Responsive layout
- Microphone recording button
- Recording animation
- Processing status
- AI response display
- Conversation reset button

---

## 🪟 Glassmorphism Design

For the main assistant card, I used a **Glassmorphism** style.

The card includes:

- Semi-transparent background
- Background blur
- Soft border
- Glow effects
- Rounded corners
- Layered shadows

This creates a modern glass-like interface while keeping the content readable.

---

# 🖥️ Interface Preview

## Frontend Interface

<img width="1819" height="938" alt="frontend" src="https://github.com/user-attachments/assets/74926742-6803-445d-b688-67407607e747" />


## Sending Voice Request

<img width="1762" height="893" alt="sending_request" src="https://github.com/user-attachments/assets/e7fbd612-31f8-456f-ba73-ba52a68c594c" />

## Arabic Response

<img width="1730" height="892" alt="arabic_result" src="https://github.com/user-attachments/assets/831f106e-90bc-46e7-9683-96fb2d6280a2" />

## English Response

<img width="1687" height="865" alt="english_result" src="https://github.com/user-attachments/assets/73711858-cf7f-4564-8e2f-86916e0111a0" />

---

# 🎥 Project Demo

The demo shows the complete Voice-to-Voice interaction.



https://github.com/user-attachments/assets/33b64ce1-88cc-471e-ba8c-8e3a40e34c65


---

# ⚙️ System Architecture

```text
User Voice
    │
    ▼
Browser MediaRecorder API
    │
    ▼
React Frontend
    │
    ▼
FastAPI Backend
    │
    ▼
Gemini Speech-to-Text
    │
    ▼
Gemini 3.6 Flash
    │
    ▼
Smart Methods Local Knowledge
    │
    ▼
AI Text Response
    │
    ▼
Gemini Text-to-Speech
    │
    ▼
Voice Response
```

---

# 🔄 Application Workflow

```text
1. User clicks the microphone button
2. The browser starts recording
3. User speaks
4. User clicks the microphone again to stop recording
5. React sends the recorded audio to FastAPI
6. Gemini converts the audio into text
7. The spoken language is detected
8. The text is sent to Gemini 3.6 Flash
9. Smart Methods reference information is provided to the model
10. The model generates a response
11. Gemini Text-to-Speech converts the response into audio
12. FastAPI returns the generated audio to React
13. The browser plays the response automatically
```

---

# 🧰 Technologies Used

## Frontend

- React
- Vite
- Tailwind CSS
- JavaScript
- Lucide React
- Browser MediaRecorder API

## Backend

- Python
- FastAPI
- Uvicorn
- python-dotenv
- python-multipart

## Artificial Intelligence

- Google Gemini
- Gemini Audio Understanding
- Gemini 3.6 Flash
- Gemini 3.1 Flash TTS Preview
- Kore Voice

## Knowledge Processing

- Local Smart Methods knowledge base
- Closed-domain company chatbot
- RAG-lite
- Local Markdown knowledge source

---

# 🧪 Task Implementation Summary

| Required Stage | Suggested Resources | Final Implementation |
|---|---|---|
| Speech-to-Text | Whisper / RealtimeSTT | Google Gemini Audio |
| LLM Processing | OpenAI / Cohere / LangChain | Gemini 3.6 Flash |
| Text-to-Speech | RealtimeTTS / Python TTS | Gemini 3.1 Flash TTS Preview |
| Voice Recording | Microphone | Browser MediaRecorder API |
| Backend | Python | FastAPI |
| Frontend | Not specified | React + Vite + Tailwind CSS |
| Company Knowledge | Not specified | Local Smart Methods Knowledge Base |
| Chat Type | General LLM | Closed-Domain Company Chatbot |
| Knowledge Method | — | RAG-Lite |

> The suggested tools were used as references and implementation options. The final project follows the same required Speech-to-Text → LLM Processing → Text-to-Speech workflow using Gemini-based services.

---

# 🌐 API Structure

The FastAPI backend runs locally at:

```text
http://127.0.0.1:8000
```

The React frontend runs locally at:

```text
http://localhost:5173
```

## Voice Endpoint

```text
POST /api/voice
```

This endpoint:

- Receives the recorded audio
- Converts speech into text
- Generates an AI response
- Converts the response into speech
- Returns the result to the frontend

## Reset Endpoint

```text
POST /api/reset
```

This clears the current conversation history.

---

# ▶️ Running the Project

## Backend

Open the first terminal:

```bash
cd backend
```

Activate the Python virtual environment if needed.

Then run:

```bash
python app.py
```

The backend will run at:

```text
http://127.0.0.1:8000
```

---

## Frontend

Open another terminal:

```bash
cd frontend
```

Install the frontend dependencies:

```bash
npm install
```

Then run:

```bash
npm run dev
```

Open:

```text
http://localhost:5173
```

---

# 🔐 Environment Variables

Create:

```text
backend/.env
```

Example:

```env
LLM_PROVIDER=gemini
GEMINI_API_KEY=YOUR_GEMINI_API_KEY
GEMINI_MODEL=gemini-3.6-flash
TTS_PROVIDER=gemini
GEMINI_TTS_MODEL=gemini-3.1-flash-tts-preview
GEMINI_VOICE=Kore
```

The real `.env` file must not be uploaded to GitHub.

Use `.env.example` to document the required variables without exposing the API key.

---

# 📦 Python Requirements

```text
python-dotenv
google-genai
fastapi
uvicorn
python-multipart
soundfile
numpy
```

Install them using:

```bash
pip install -r requirements.txt
```

---

# ✨ Final Result

The final project is a complete bilingual **Voice-to-Voice AI Assistant** that combines:

```text
Voice Interaction
+
Speech Recognition
+
Large Language Model
+
Internal Company Knowledge
+
Text-to-Speech
+
Modern Web Interface
```

The project started as a simple Python, Gradio, and CSS implementation, then evolved into a separated **React frontend and FastAPI backend** architecture.

This redesign improved project organization, provided more control over the interface, and allowed the final application to use a modern Glassmorphism-style user experience.

---

#  Training Context

This project was developed as part of a **Robotics Engineering training task **.

The task combines:

- Artificial Intelligence
- Voice Processing
- LLM Integration
- Web Development
- Backend APIs
- Human-Robot Interaction
