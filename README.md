# FreeFlow LLM bridge

FastAPI service that exposes a `/chat` endpoint compatible with the help-center backend when using the FreeFlow LLM provider.

## Setup

1. Copy env example and add your API keys:
   ```bash
   cp .env.example .env
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Run (so the backend can connect)

1. **Backend** must use the same port. In `backend/.env` set:
   ```bash
   FREEFLOW_SERVICE_URL=http://localhost:8000
   ```
   (If you omit it, the backend defaults to 8000.)

2. **Start the Python service** from the project root, or from inside `freeflow-service`:
   ```bash
   cd freeflow-service
   python main.py
   ```
   It listens on **http://127.0.0.1:8000**. You should see something like: `Uvicorn running on http://127.0.0.1:8000`.

3. Start the backend (`cd backend` then `npm run start:dev` or `pnpm run start:dev`). Chat requests will call this service.

**If your backend `.env` uses port 8001** instead, run the Python service on 8001:
   - **PowerShell:** `$env:PORT="8001"; python main.py`
   - **Or** add `PORT=8001` to `freeflow-service/.env`, then run `python main.py`.

Set at least one of `GROQ_API_KEY` or `GEMINI_API_KEY` in `freeflow-service/.env`.

### Production

- Set **`HOST=0.0.0.0`** (and optionally `PORT`) in `.env` so the service is reachable from other hosts/containers. Default `127.0.0.1` is for local dev only.
- Ensure the **backend** has `FREEFLOW_SERVICE_URL` set to this service’s URL (e.g. `http://freeflow-service:8000` or your public URL).
