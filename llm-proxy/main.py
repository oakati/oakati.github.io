"""
LLM Proxy - Ollama'ya rate-limited, CORS-protected proxy.
IP başına günde 5 istek; Origin/Referer kontrolü; streaming desteği.
"""
import json
import re
from collections import defaultdict
from datetime import date
from typing import Optional

from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import httpx

app = FastAPI()

# CORS - sadece site ve localhost
ALLOWED_ORIGINS = [
    "https://oakati.github.io",
    "http://localhost:4000",
    "http://127.0.0.1:4000",
]
ALLOWED_ORIGIN_PATTERN = re.compile(
    r"^https://oakati\.github\.io($|/)|^http://localhost(:\d+)?($|/)|^http://127\.0\.0\.1(:\d+)?($|/)"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["POST", "OPTIONS"],
    allow_headers=["*"],
)

OLLAMA_URL = "http://localhost:11434"
OLLAMA_MODEL = "qwen2.5:0.5b"
BODY_LIMIT = 16 * 1024  # 16 KB
OLLAMA_TIMEOUT = 90.0
RATE_LIMIT_PER_DAY = 5

# ip -> (date, count)
rate_limit: dict[str, tuple[date, int]] = defaultdict(lambda: (date.today(), 0))


def get_client_ip(request: Request) -> str:
    """Gerçek istemci IP'sini al (tünel header'larından)."""
    forwarded = request.headers.get("X-Forwarded-For") or request.headers.get("CF-Connecting-IP")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.client.host if request.client else "unknown"


def check_origin(request: Request) -> bool:
    """Origin veya Referer izin verilen site ile eşleşmeli."""
    origin = request.headers.get("Origin")
    referer = request.headers.get("Referer")
    for val in (origin, referer):
        if val and ALLOWED_ORIGIN_PATTERN.search(val.split("?")[0].rstrip("/")):
            return True
    return False


def check_rate_limit(ip: str) -> None:
    """Rate limit kontrolü; aşılırsa 429."""
    today = date.today()
    stored_date, count = rate_limit[ip]
    if stored_date != today:
        stored_date, count = today, 0
        rate_limit[ip] = (today, 0)
    if count >= RATE_LIMIT_PER_DAY:
        raise HTTPException(status_code=429, detail="Günlük istek limiti aşıldı (5/gün)")
    rate_limit[ip] = (stored_date, count + 1)


@app.post("/chat")
async def chat(request: Request):
    # Origin/Referer
    if not check_origin(request):
        raise HTTPException(status_code=401, detail="Unauthorized origin")

    # Rate limit
    ip = get_client_ip(request)
    check_rate_limit(ip)

    # Body limit (Content-Length + read limit)
    cl = request.headers.get("Content-Length")
    if cl:
        try:
            if int(cl) > BODY_LIMIT:
                raise HTTPException(status_code=413, detail="Request body too large")
        except ValueError:
            pass
    body = b""
    async for chunk in request.stream():
        body += chunk
        if len(body) > BODY_LIMIT:
            raise HTTPException(status_code=413, detail="Request body too large")

    try:
        data = json.loads(body)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON")

    # messages veya message
    messages = data.get("messages")
    if not messages:
        msg = data.get("message", "")
        if not isinstance(msg, str):
            raise HTTPException(status_code=400, detail="message must be string")
        messages = [{"role": "user", "content": msg}]
    else:
        if not isinstance(messages, list):
            raise HTTPException(status_code=400, detail="messages must be array")
        for m in messages:
            if not isinstance(m, dict) or "role" not in m or "content" not in m:
                raise HTTPException(status_code=400, detail="Invalid message format")

    # Ollama chat stream
    ollama_payload = {
        "model": OLLAMA_MODEL,
        "messages": messages,
        "stream": True,
    }

    async def stream_response():
        async with httpx.AsyncClient(timeout=OLLAMA_TIMEOUT) as client:
            async with client.stream(
                "POST",
                f"{OLLAMA_URL}/api/chat",
                json=ollama_payload,
            ) as resp:
                if resp.status_code != 200:
                    err = await resp.aread()
                    yield f"data: {json.dumps({'error': err.decode()})}\n\n"
                    return
                async for line in resp.aiter_lines():
                    if line:
                        yield f"data: {line}\n\n"

    return StreamingResponse(
        stream_response(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )
