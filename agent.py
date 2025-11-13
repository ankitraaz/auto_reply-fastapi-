# app/agent.py
from typing import List, Dict

SYSTEM_PROMPT = """You are a helpful, concise AI agent. 
- Answer clearly.
- Ask one clarifying question if needed.
- Tag intent and sentiment in metadata."""

async def agent_reply(thread_id: str, user_text: str) -> str:
    context = await fetch_recent_messages(thread_id, limit=10)
    prompt = build_prompt(SYSTEM_PROMPT, context, user_text)
    # Swap provider here: Gemini/OpenAI/local
    return await call_llm(prompt)

def build_prompt(system: str, history: List[Dict], user: str) -> str:
    parts = [f"System:\n{system}\n"]
    for m in history:
        parts.append(f"{m['role'].title()}: {m['content']}\n")
    parts.append(f"User: {user}\nAssistant:")
    return "".join(parts)
