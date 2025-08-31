from telegram.ext import Application, CommandHandler, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import os

# Bot-Token aus Umgebungsvariablen
TOKEN = os.getenv("TELEGRAM_TOKEN")

async def start(update, context):
    await update.message.reply_text("Hallo! Ich bin dein iPad-Bot! 😊")

async def hello(update, context):
    await update.message.reply_text("Hey, wie geht’s? Probiere /start!")

async def dashboard(update, context):
    # Definiere Buttons für verfügbare Befehle
    keyboard = [
        [
            InlineKeyboardButton("Start", callback_data="cmd_start"),
            InlineKeyboardButton("Hello", callback_data="cmd_hello"),
        ],
        [InlineKeyboardButton("Hilfe", callback_data="cmd_help")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Wähle einen Befehl aus:", reply_markup=reply_markup
    )

async def button_callback(update, context):
    query = update.callback_query
    await query.answer()  # Bestätige den Button-Klick
    if query.data == "cmd_start":
        await query.message.reply_text("Hallo! Ich bin dein iPad-Bot! 😊")
    elif query.data == "cmd_hello":
        await query.message.reply_text("Hey, wie geht’s? Probiere /start!")
    elif query.data == "cmd_help":
        await query.message.reply_text("Verfügbare Befehle: /start, /hello, /dashboard")

def main():
    # Erstelle die Application
    app = Application.builder().token(TOKEN).build()

    # Füge Befehle hinzu
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("hello", hello))
    app.add_handler(CommandHandler("dashboard", dashboard))
    app.add_handler(CallbackQueryHandler(button_callback))

    # Starte Webhook
    app.run_webhook(
        listen="0.0.0.0",
        port=int(os.getenv("PORT", 8443)),
        url_path=TOKEN,
        webhook_url=f"https://{os.getenv('RENDER_EXTERNAL_HOSTNAME')}/{TOKEN}"
    )

if __name__ == "__main__":
    main()