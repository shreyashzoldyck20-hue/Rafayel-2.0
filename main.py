from uuid import uuid4
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .db import init_db, connect
from .schemas import ChatRequest, ChatResponse, MemoryRequest
from .emotion import detect_tone, style_instruction
from .providers import chat, ProviderError

app = FastAPI(title="RAFAYEL API", version="0.1.0")
app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_credentials=False,
    allow_methods=["GET", "POST", "DELETE"], allow_headers=["*"]
)

@app.on_event("startup")
def startup():
    init_db()

@app.get("/health")
def health():
    return {"status": "ok", "name": "RAFAYEL", "version": "0.1.0"}

@app.post("/api/chat", response_model=ChatResponse)
async def send_chat(body: ChatRequest):
    cid = body.conversation_id or str(uuid4())
    tone = detect_tone(body.message)
    with connect() as db:
        history = db.execute(
            "SELECT role, content FROM messages WHERE conversation_id=? ORDER BY id DESC LIMIT 12",
            (cid,)
        ).fetchall()
        memories = db.execute("SELECT content FROM memories ORDER BY id DESC LIMIT 12").fetchall()
        db.execute("INSERT INTO messages(conversation_id, role, content) VALUES(?,?,?)",
                   (cid, "user", body.message))
    system = (
        "You are RAFAYEL, a helpful personal AI assistant. Speak naturally and clearly. "
        "You may adapt your tone to the user's emotional cues, but do not claim to have human "
        "emotions, consciousness, or a personal relationship. Explain uncertainty honestly. "
        "Never claim an action was performed unless a connected tool actually performed it. "
        "Do not execute or suggest unsafe computer actions. "
        + style_instruction(tone)
    )
    if memories:
        system += "\nUser-approved memory notes (use only when relevant): " + "; ".join(m["content"] for m in memories)
    messages = [{"role": "system", "content": system}]
    messages += [{"role": row["role"], "content": row["content"]} for row in reversed(history)]
    messages.append({"role": "user", "content": body.message})
    try:
        reply, provider = await chat(messages)
    except ProviderError as exc:
        raise HTTPException(status_code=503, detail=str(exc))
    with connect() as db:
        db.execute("INSERT INTO messages(conversation_id, role, content) VALUES(?,?,?)",
                   (cid, "assistant", reply))
    return ChatResponse(conversation_id=cid, reply=reply, provider=provider, emotional_tone=tone)

@app.get("/api/history/{conversation_id}")
def history(conversation_id: str):
    with connect() as db:
        rows = db.execute(
            "SELECT role, content, created_at FROM messages WHERE conversation_id=? ORDER BY id",
            (conversation_id,)
        ).fetchall()
    return [dict(r) for r in rows]

@app.post("/api/memories")
def save_memory(body: MemoryRequest):
    with connect() as db:
        cur = db.execute("INSERT INTO memories(content) VALUES(?)", (body.content,))
        return {"id": cur.lastrowid, "content": body.content}

@app.get("/api/memories")
def list_memories():
    with connect() as db:
        return [dict(r) for r in db.execute("SELECT id, content, created_at FROM memories ORDER BY id DESC")]

@app.delete("/api/memories/{memory_id}")
def delete_memory(memory_id: int):
    with connect() as db:
        cur = db.execute("DELETE FROM memories WHERE id=?", (memory_id,))
        if cur.rowcount == 0:
            raise HTTPException(status_code=404, detail="Memory not found")
    return {"deleted": True}
