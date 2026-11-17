# RAFAYEL — Hybrid Personal AI Assistant

A starter monorepo for **Windows desktop + Android** with a shared FastAPI brain.

## What works in this starter
- Text chat from the desktop and Android clients.
- Hybrid model routing: try a configured cloud OpenAI-compatible endpoint; fall back to a local Ollama model.
- SQLite conversation history and user-approved memories.
- Lightweight emotional-tone detection to adapt response style (not a claim that the AI has feelings).
- Explicit permission gate for future computer-control tools. No hidden automation is enabled.
- Health endpoint and simple setup scripts.

## Architecture
```
RAFAYEL/
  backend/       FastAPI API, model router, SQLite memory
  desktop/       Electron + React + TypeScript desktop client
  android/       Native Android app (Kotlin + Jetpack Compose)
  docs/          setup and security notes
```

Both clients call the same backend. For Android, use the PC's LAN IP while both devices are on the same Wi-Fi.

## Requirements
- Python 3.11+
- Node.js 20+
- Android Studio (for Android build)
- Optional local model: Ollama
- Optional cloud model: an OpenAI-compatible API key and base URL

## 1. Start the backend (Windows PowerShell)
```powershell
cd backend
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```
Open `http://127.0.0.1:8000/health`.

Edit `backend/.env`:
- `CLOUD_BASE_URL` e.g. your provider's `/v1` endpoint
- `CLOUD_API_KEY`
- `CLOUD_MODEL`
- `OLLAMA_BASE_URL` (default `http://127.0.0.1:11434`)
- `OLLAMA_MODEL` (default `qwen2.5:3b`)

For local fallback, install Ollama and pull a model:
```powershell
ollama pull qwen2.5:3b
```
If neither cloud nor local model is available, the API returns a clear setup error.

## 2. Run the desktop app
In a second terminal:
```powershell
cd desktop
npm install
npm run dev
```
The desktop UI expects the backend at `http://127.0.0.1:8000`.

To package later:
```powershell
npm run build
npm run package
```

## 3. Run Android
Open `android/` in Android Studio, allow Gradle sync, then run the `app` configuration.
Set `API_BASE_URL` in `android/gradle.properties` to your PC LAN address, for example:
`API_BASE_URL=http://192.168.1.20:8000/`
The Android device and PC must be on the same Wi-Fi. For a production release, use HTTPS and authentication; do not expose this development server directly to the public internet.

## API
- `GET /health`
- `POST /api/chat` — `{ "message": "...", "conversation_id": "optional-id" }`
- `GET /api/history/{conversation_id}`
- `POST /api/memories` — save a user-approved memory
- `GET /api/memories`
- `DELETE /api/memories/{memory_id}`

## Important security boundaries
This is a working chat-and-memory foundation, not a finished autonomous PC operator.
- No shell, arbitrary file, browser, camera, microphone, or screen-control tool is exposed.
- Add future tools behind explicit allowlists, scoped permissions, visible confirmation, timeouts, and audit logs.
- Keep API keys in backend `.env`, never in either client.
- The development API has no authentication. Keep it on a trusted private network only.
