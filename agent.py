from typing import List, Dict
import os
import google.generativeai as genai
from sqlalchemy.future import select
from database import SessionLocal

from models import Message

SYSTEM_PROMPT = """You are a helpful, concise AI agent. 
- Answer clearly.
- Ask one clarifying question if needed.
- Tag intent and sentiment in metadata."""

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

async def fetch_recent_messages(thread_id: str, limit: int = 10):
    async with SessionLocal() as session:
        result = await session.execute(
            select(Message).where(Message.thread_id == thread_id).order_by(Message.id.desc()).limit(limit)
        )
        rows = result.scalars().all()
        return [{"role": m.role, "content": m.content} for m in rows]

async def save_message(thread_id: str, role: str, content: str):
    async with SessionLocal() as session:
        msg = Message(thread_id=thread_id, role=role, content=content)
        session.add(msg)
        await session.commit()

async def call_llm(prompt: str) -> str:
    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"🤖 AI error: {str(e)}"

async def agent_reply(thread_id: str, user_text: str) -> str:
    context = await fetch_recent_messages(thread_id, limit=10)
    prompt = build_prompt(SYSTEM_PROMPT, context, user_text)
    reply = await call_llm(prompt)
    await save_message(thread_id, "assistant", reply)
    return reply

def build_prompt(system: str, history: List[Dict], user: str) -> str:
    parts = [f"System:\n{system}\n"]
    for m in history:
        parts.append(f"{m['role'].title()}: {m['content']}\n")
    parts.append(f"User: {user}\nAssistant:")
    return "".join(parts)
