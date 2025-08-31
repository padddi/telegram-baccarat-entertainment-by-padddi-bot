from telegram.ext import Application, CommandHandler
import os

# Bot-Token aus Umgebungsvariablen
TOKEN = os.getenv("TELEGRAM_TOKEN")

async def start(update, context):
    await update.message.reply_text("Hallo! Ich heiße dich herzlich Willkommen! 😊")

async def hello(update, context):
    await update.message.reply_text("Hey, wie geht’s? Probiere /start!")

def main():
    # Erstelle die Application
    app = Application.builder().token(TOKEN).build()

    # Füge Befehle hinzu
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("hello", hello))

    # Starte Webhook
    app.run_webhook(
        listen="0.0.0.0",
        port=int(os.getenv("PORT", 8443)),
        url_path=TOKEN,
        webhook_url=f"https://{os.getenv('RENDER_EXTERNAL_HOSTNAME')}/{TOKEN}"
    )

if __name__ == "__main__":
    main()