### File: backend/main.py

from fastapi import FastAPI, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import replicate
import openai
import tempfile
import subprocess
import os
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi import Request

app = FastAPI()

app.mount("/static", StaticFiles(directory="frontend"), name="static")

# Allow frontend to access backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Set API keys
REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY


# Convert uploaded audio to WAV format (mono, 16kHz)
def convert_audio_to_wav(uploaded_file):
    input_temp = tempfile.NamedTemporaryFile(delete=False, suffix=".input")
    input_temp.write(uploaded_file.file.read())
    input_temp.flush()

    output_temp = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    subprocess.run([
        "ffmpeg", "-y",
        "-i", input_temp.name,
        "-ar", "16000",
        "-ac", "1",
        output_temp.name
    ], check=True)

    return output_temp.name

@app.get("/", response_class=HTMLResponse)
async def serve_index():
    with open("frontend/index.html", "r") as f:
        return f.read()

@app.post("/process")
async def process_audio(
    file: UploadFile,
    input_language: str = Form(None),
    target_language: str = Form("en"),
    diarize: bool = Form(True),
    custom_prompt: str = Form(None)
):
    try:
        wav_path = convert_audio_to_wav(file)

        # WhisperX transcription
        with open(wav_path, "rb") as audio_file:
            output = replicate.run(
                "student0129/whisperx-replicate-from-github:latest",
                input={
                    "audio": audio_file,
                    "task": "transcribe",
                    "language": input_language if input_language else None,
                    "diarize": diarize,
                    "align_output": False
                }
            )

        transcript_segments = output["segments"]
        transcript = "\n".join(
            f"{s.get('speaker', 'Unknown')}: {s['text']}" if diarize else s['text']
            for s in transcript_segments
        )

        # Translate using GPT-4o (if needed)
        if input_language and input_language == target_language:
            translated = transcript
        else:
            trans_prompt = f"Translate this into {target_language}:\n\n{transcript}"
            translated = openai.ChatCompletion.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": trans_prompt}],
                temperature=0.3
            )["choices"][0]["message"]["content"]

        # Summarize
        summary_prompt = custom_prompt or "Summarize the key points, decisions, and any action items in this conversation:"
        full_prompt = f"{summary_prompt}\n\n{translated}"

        summary = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": full_prompt}
            ],
            temperature=0.4,
            max_tokens=700
        )["choices"][0]["message"]["content"]

        return JSONResponse({
            "transcript": transcript,
            "translated": translated,
            "summary": summary
        })

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
