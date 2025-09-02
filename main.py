# main.py
import os
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from handlers import start, dashboard, info, refresh, result, daily, weekly, monthly, yearly, chatid, subscribe, unsubscribe, handle_keyboard_buttons

def main():
    # Bot-Token aus Umgebungsvariablen
    TOKEN = os.getenv("TELEGRAM_TOKEN")
    
    # Initialisiere die Telegram-Applikation
    app = Application.builder().token(TOKEN).build()
    
    # Füge Handler hinzu
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("dashboard", dashboard))
    app.add_handler(CommandHandler("info", info))
    app.add_handler(CommandHandler("result", result))
    app.add_handler(CommandHandler("daily", daily))
    app.add_handler(CommandHandler("weekly", weekly))
    app.add_handler(CommandHandler("monthly", monthly))
    app.add_handler(CommandHandler("yearly", yearly))
    app.add_handler(CommandHandler("refresh", refresh))
    app.add_handler(CommandHandler("chatid", chatid))
    app.add_handler(CommandHandler("subscribe", subscribe))    # Neuer Handler
    app.add_handler(CommandHandler("unsubscribe", unsubscribe))  # Neuer Handler
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_keyboard_buttons))
    
    # Starte den Webhook
    app.run_webhook(
        listen="0.0.0.0",
        port=int(os.getenv("PORT", 8443)),
        url_path=TOKEN,
        webhook_url=f"https://{os.getenv('RENDER_EXTERNAL_HOSTNAME')}/{TOKEN}"
    )

if __name__ == "__main__":
    main()