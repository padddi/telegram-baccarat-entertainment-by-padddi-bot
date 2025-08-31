from datetime import datetime, timedelta
from telegram import ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters
import os

# Bot-Token aus Umgebungsvariablen
TOKEN = os.getenv("TELEGRAM_TOKEN")

# Globale Konstanten
KEYBOARD = ReplyKeyboardMarkup([
    ["ℹ️ Info", "📈 Letztes Ergebnis"],
    ["📅 Ergebnisse (Aktuelle Woche)", "🗓️ Ergebnisse (Monate)"],
    ["🗂️ Ergebnisse (Aktuelles Jahr)"]
], resize_keyboard=True)

WEEKDAYS = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag"]

DASHBOARD_MESSAGE = (
    "*📊 Dein Bot-Dashboard 📊*\n\n"
    "Willkommen im BE Bot Dashboard. Du hast folgende Möglichkeiten zur Auswahl:\n\n"
    "ℹ️ *Info*: Zeigt Infos zum Bot\n"
    "Befehl: /info\n\n"
    "📈 *Result*: Zeigt das letzte Ergebnis\n"
    "Befehl: /result\n\n"
    "📅 *Daily*: Ergebnisse dieser Woche\n"
    "Befehl: /daily\n\n"
    "🗓️ *Weekly*: Ergebnisse aller Wochen\n"
    "Befehl: /weekly\n\n"
    "🗂️ *Yearly*: Ergebnisse des Jahres\n"
    "Befehl: /yearly\n\n"
    "Bitte wähle einen Befehl aus dem unteren Menü."
)

async def start(update, context):
    await update.message.reply_text(DASHBOARD_MESSAGE, reply_markup=KEYBOARD, parse_mode="Markdown")

async def dashboard(update, context):
    await update.message.reply_text(DASHBOARD_MESSAGE, reply_markup=KEYBOARD, parse_mode="Markdown")

async def info(update, context):
    await update.message.reply_text(DASHBOARD_MESSAGE, reply_markup=KEYBOARD, parse_mode="Markdown")

async def result(update, context):
    result_percent = "1.04"  # PLATZHALTER_RESULT_PERCENT: Ersetze mit echtem Wert
    today = datetime.now().strftime("%d.%m.%Y")
    message = f"📈 *Letztes Ergebnis vom {today}*\n\n✅ {result_percent}%"
    await update.message.reply_text(message, reply_markup=KEYBOARD, parse_mode="Markdown")

async def daily(update, context):
    today = datetime.now()
    week_start = today - timedelta(days=today.weekday())
    results = {  # PLATZHALTER_DAILY_RESULTS: Ersetze mit echten Daten
        (week_start + timedelta(days=i)).strftime("%d.%m.%Y"): f"{1.00 + i * 0.1:.2f}"
        for i in range(5)  # Nur Montag bis Freitag
    }
    message = "📅 *Ergebnisse der aktuellen Woche*\n\n"
    for i, (date, result) in enumerate(results.items()):
        message += f"{date}, {WEEKDAYS[i]}: {result}%\n"
    await update.message.reply_text(message, reply_markup=KEYBOARD, parse_mode="Markdown")

async def weekly(update, context):
    today = datetime.now()
    current_week = today.isocalendar().week  # Aktuelle Woche (z. B. 35 für 31.08.2025)
    results = {  # PLATZHALTER_WEEKLY_RESULTS: Ersetze mit echten Daten
        f"Woche {i+1}": f"{1.00 + i * 0.05:.2f}" for i in range(current_week)
    }
    message = "🗓️ *Ergebnisse (Monate)*\n\n"
    for week, result in results.items():
        message += f"{week}: {result}%\n"
    await update.message.reply_text(message, reply_markup=KEYBOARD, parse_mode="Markdown")

async def yearly(update, context):
    results = [  # PLATZHALTER_YEARLY_RESULTS: Ersetze mit echten Daten
        ("2025", "1.50")
    ]
    message = "🗂️ *Ergebnisse (Jahre)*\n\n"
    for year, result in results:
        message += f"{year}: {result}%"
    await update.message.reply_text(message, reply_markup=KEYBOARD, parse_mode="Markdown")

async def handle_keyboard_buttons(update, context):
    text = update.message.text
    if text == "ℹ️ Info":
        await info(update, context)
    elif text == "📈 Letztes Ergebnis":
        await result(update, context)
    elif text == "📅 Ergebnisse (Aktuelle Woche)":
        await daily(update, context)
    elif text == "🗓️ Ergebnisse (Monate)":
        await weekly(update, context)
    elif text == "🗂️ Ergebnisse (Aktuelles Jahr)":
        await yearly(update, context)
    else:
        await update.message.reply_text(
            "Bitte wähle einen Befehl aus dem unteren Menü.",
            reply_markup=KEYBOARD
        )

def main():
    app = Application.builder().token(TOKEN).build()

    # Befehle hinzufügen
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("dashboard", dashboard))
    app.add_handler(CommandHandler("info", info))
    app.add_handler(CommandHandler("result", result))
    app.add_handler(CommandHandler("daily", daily))
    app.add_handler(CommandHandler("weekly", weekly))
    app.add_handler(CommandHandler("yearly", yearly))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_keyboard_buttons))

    # Webhook starten
    app.run_webhook(
        listen="0.0.0.0",
        port=int(os.getenv("PORT", 8443)),
        url_path=TOKEN,
        webhook_url=f"https://{os.getenv('RENDER_EXTERNAL_HOSTNAME')}/{TOKEN}"
    )

if __name__ == "__main__":
    main()