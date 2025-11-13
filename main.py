from fastapi import FastAPI, Request
import os
import logging
from dotenv import load_dotenv
from deliver import deliver
from agent import agent_reply   # Gemini smart reply
from crud import save_message   # DB insert

load_dotenv()
logging.basicConfig(level=logging.INFO)

app = FastAPI()

@app.get("/")
def root():
    logging.info("✅ Root route hit")
    return {"status": "ok", "message": "FastAPI backend is live!"}

@app.post("/webhook/telegram")
async def telegram_webhook(req: Request):
    logging.info("📩 Telegram webhook triggered")
    data = await req.json()
    logging.info(f"📦 Payload: {data}")

    message = data.get("message", {})
    chat_id = message.get("chat", {}).get("id")
    user_text = message.get("text", "")
    thread_id = str(chat_id)

    if chat_id and user_text:
        # Try Gemini smart reply
        try:
            reply = await agent_reply(thread_id, user_text)
            logging.info(f"🤖 Gemini reply: {reply}")
        except Exception as e:
            logging.warning(f"⚠️ Gemini failed: {e}")
            reply = f"Echo: {user_text}"

        # Deliver reply
        await deliver("telegram", chat_id, reply)
        logging.info(f"📤 Sent reply: {reply}")

        # Save to DB
        try:
            await save_message(thread_id, "user", user_text, "telegram")
            await save_message(thread_id, "bot", reply, "telegram")
            logging.info("🗂️ Messages saved to DB")
        except Exception as e:
            logging.warning(f"⚠️ DB save failed: {e}")

    return {"ok": True}

@app.post("/webhook/message")
async def generic_webhook(req: Request):
    logging.info("📩 Generic webhook triggered")
    data = await req.json()
    logging.info(f"📦 Payload: {data}")

    user_id = data.get("user_id")
    platform = data.get("platform")
    text = data.get("text")
    thread_id = data.get("thread_id")

    if user_id and platform and text:
        try:
            reply = await agent_reply(thread_id, text)
            logging.info(f"🤖 Gemini reply: {reply}")
        except Exception as e:
            logging.warning(f"⚠️ Gemini failed: {e}")
            reply = f"Echo: {text}"

        await deliver(platform, user_id, reply)
        logging.info(f"📤 Sent reply: {reply}")

        try:
            await save_message(thread_id, "user", text, platform)
            await save_message(thread_id, "bot", reply, platform)
            logging.info("🗂️ Messages saved to DB")
        except Exception as e:
            logging.warning(f"⚠️ DB save failed: {e}")

    return {"ok": True}

@app.post("/{path:path}")
async def catch_all(path: str, req: Request):
    logging.warning(f"⚠️ Unknown POST route hit: /{path}")
    return {"error": "Invalid route"}
