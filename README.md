# WhisperX Audio Summarizer

A simple web app that lets users upload audio files, transcribe them using Replicate's WhisperX, optionally translate the content, and summarize it using GPT-4o. Includes speaker diarization and support for custom summary prompts.

## 🌐 Live Demo (Optional)
> [Add your frontend GitHub Pages or Render static site URL here]

---

## 📦 Features

- Upload audio in any format (MP3, WAV, M4A, etc.)
- Auto-convert to WhisperX-compatible format
- Transcription with optional speaker diarization
- Translation to any destination language (default is English)
- Summary generation using GPT-4o with customizable prompts
- Clean, minimal frontend using HTML + JS + CSS

---

## 🗂 Project Structure

```
/
├── backend/
│   ├── main.py              # FastAPI server
│   ├── requirements.txt
│   ├── Dockerfile
│
├── frontend/
│   ├── index.html
│   ├── script.js
│   └── style.css
│
├── .gitignore
├── render.yaml              # Render deployment config
└── README.md
```

---

## 🚀 Quick Start (Local Dev)

1. **Clone the repo**
```bash
git clone https://github.com/your-username/whisperx-audio-summarizer.git
cd whisperx-audio-summarizer/backend
```

2. **Create a `.env` file**
```
REPLICATE_API_TOKEN=your_replicate_token
OPENAI_API_KEY=your_openai_key
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run the app**
```bash
python main.py
```

5. **Open the frontend**
Open `frontend/index.html` in your browser and point the JS `fetch()` URL to `http://localhost:8000/process`.

---

## ☁️ Deploying to Render

1. Push this repo to GitHub
2. Go to [Render](https://render.com) → New Web Service → "From GitHub"
3. Select your repo
4. Render will detect `render.yaml` and auto-configure
5. Add these environment variables in Render dashboard:
   - `REPLICATE_API_TOKEN`
   - `OPENAI_API_KEY`

---

## 🔗 Dependencies

- [Replicate](https://replicate.com/m-bain/whisperx)
- [OpenAI API (GPT-4o)](https://platform.openai.com/docs/models/gpt-4o)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Render](https://render.com/)
- [ffmpeg](https://ffmpeg.org/)

---

## 📋 License

MIT License
