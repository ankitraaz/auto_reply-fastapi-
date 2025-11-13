import os
import httpx
from twilio.rest import Client

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_API = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP_NUMBER = os.getenv("TWILIO_WHATSAPP_NUMBER")

SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")

async def telegram_send(user_id: str, text: str):
    async with httpx.AsyncClient() as client:
        resp = await client.post(TELEGRAM_API, json={
            "chat_id": user_id,
            "text": text
        })
        print("📤 Telegram response:", resp.status_code, resp.text)

async def twilio_whatsapp_send(user_id: str, text: str):
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    message = client.messages.create(
        from_=f"whatsapp:{TWILIO_WHATSAPP_NUMBER}",
        to=f"whatsapp:{user_id}",
        body=text
    )
    print("📤 WhatsApp SID:", message.sid)

async def slack_send(user_id: str, text: str):
    async with httpx.AsyncClient() as client:
        resp = await client.post(SLACK_WEBHOOK_URL, json={"text": text})
        print("📤 Slack response:", resp.status_code, resp.text)

async def deliver(platform: str, user_id: str, text: str):
    if platform == "telegram":
        await telegram_send(user_id, text)
    elif platform == "whatsapp":
        await twilio_whatsapp_send(user_id, text)
    elif platform == "slack":
        await slack_send(user_id, text)
    else:
        return {"status": "ok", "message": text}
