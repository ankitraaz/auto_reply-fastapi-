# app/deliver.py
async def deliver(platform: str, user_id: str, text: str):
    if platform == "telegram":
        await telegram_send(user_id, text)
    elif platform == "whatsapp":
        await twilio_whatsapp_send(user_id, text)
    elif platform == "slack":
        await slack_send(user_id, text)
    else:
        pass  # web: return in HTTP
