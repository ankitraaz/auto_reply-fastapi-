# app/main.py
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os

app = FastAPI()

class InboundMessage(BaseModel):
    user_id: str
    platform: str  # "telegram" | "whatsapp" | "slack" | "web"
    text: str
    thread_id: str | None = None

@app.post("/webhook/message")
async def handle_message(msg: InboundMessage):
    # 1) find/create user & thread
    thread_id = msg.thread_id or await ensure_thread(msg.user_id)
    # 2) store user message
    await save_message(thread_id, role="user", content=msg.text)
    # 3) get agent reply
    reply = await agent_reply(thread_id, msg.text)
    # 4) store assistant message
    await save_message(thread_id, role="assistant", content=reply)
    # 5) deliver back to channel
    await deliver(msg.platform, msg.user_id, reply)
    return {"status": "ok"}

# Allow frontend (Flutter web) to talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # sab origins allow (basic testing ke liye)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)