from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler
from telegram.ext.filters import Filters  # Korrigierter Import für Filters
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
import os
from datetime import datetime, timedelta

# Bot-Token aus Umgebungsvariablen
TOKEN = os.getenv("TELEGRAM_TOKEN")

async def dashboard(update, context):
    # Definiere Inline-Buttons für /dashboard (im Chat)
    keyboard = [
        [InlineKeyboardButton("ℹ️ Info", callback_data="cmd_info"), InlineKeyboardButton("📈 Result", callback_data="cmd_result")],
        [InlineKeyboardButton("📅 Daily", callback_data="cmd_daily"), InlineKeyboardButton("🗓️ Weekly", callback_data="cmd_weekly")],
        [InlineKeyboardButton("🗂️ Yearly", callback_data="cmd_yearly")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    message = (
        "*📊 Dein Bot-Dashboard 📊*\n"
        "Wähle einen Befehl aus:\n\n"
        "ℹ️ *Info*: Zeigt Infos zum Bot\n"
        "📈 *Result*: Zeigt das heutige Ergebnis\n"
        "📅 *Daily*: Ergebnisse dieser Woche\n"
        "🗓️ *Weekly*: Ergebnisse aller Wochen\n"
        "🗂️ *Yearly*: Ergebnisse des Jahres"
    )
    # Entferne Custom Keyboard, um Standard-Tastatur bei /dashboard zu zeigen
    await update.message.reply_text(message, reply_markup=reply_markup, parse_mode="Markdown")

async def info(update, context):
    # Definiere Custom Keyboard
    keyboard = [
        ["ℹ️ Informationen", "📈 Heutiges Ergebnis"],
        ["📅 Ergebnisse (Aktuelle Woche)", "🗓️ Ergebnisse (Aktueller Monat)"],
        ["🗂️ Ergebnisse (Aktuelles Jahr)"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(
        "ℹ️ *Info*\n"
        "Dies ist ein Platzhaltertext für den Bot. Er beschreibt, worum es geht. "
        "#PLATZHALTER_INFO_TEXT",  # Platzhalter für späteren Info-Text
        parse_mode="Markdown",
        reply_markup=reply_markup
    )

async def result(update, context):
    # Definiere Custom Keyboard
    keyboard = [
        ["ℹ️ Informationen", "📈 Heutiges Ergebnis"],
        ["📅 Ergebnisse (Aktuelle Woche)", "🗓️ Ergebnisse (Aktueller Monat)"],
        ["🗂️ Ergebnisse (Aktuelles Jahr)"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    result_percent = "1.04"  # PLATZHALTER_RESULT_PERCENT: Ersetze mit echtem Wert
    today = datetime.now().strftime("%Y-%m-%d")  # Aktuelles Datum
    await update.message.reply_text(
        f"📈 *Das Ergebnis von heute {today}*\n"
        f"{result_percent}%",
        parse_mode="Markdown",
        reply_markup=reply_markup
    )

async def daily(update, context):
    # Definiere Custom Keyboard
    keyboard = [
        ["ℹ️ Informationen", "📈 Heutiges Ergebnis"],
        ["📅 Ergebnisse (Aktuelle Woche)", "🗓️ Ergebnisse (Aktueller Monat)"],
        ["🗂️ Ergebnisse (Aktuelles Jahr)"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    # Simuliere Ergebnisse für die aktuelle Woche (Platzhalter)
    today = datetime.now()
    week_start = today - timedelta(days=today.weekday())
    results = {  # PLATZHALTER_DAILY_RESULTS: Ersetze mit echten Daten
        (week_start + timedelta(days=i)).strftime("%Y-%m-%d"): f"{1.00 + i * 0.1:.2f}"
        for i in range(7)
    }
    # Normales Markdown-Format
    message = "📅 *Ergebnisse der aktuellen Woche*\n\n"
    for date, result in results.items():
        message += f"{date}: {result}%\n"
    await update.message.reply_text(message, parse_mode="Markdown", reply_markup=reply_markup)

async def weekly(update, context):
    # Definiere Custom Keyboard
    keyboard = [
        ["ℹ️ Informationen", "📈 Heutiges Ergebnis"],
        ["📅 Ergebnisse (Aktuelle Woche)", "🗓️ Ergebnisse (Aktueller Monat)"],
        ["🗂️ Ergebnisse (Aktuelles Jahr)"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    # Simuliere Ergebnisse für 52 Wochen (Platzhalter)
    results = {  # PLATZHALTER_WEEKLY_RESULTS: Ersetze mit echten Daten
        f"Woche {i+1}": f"{1.00 + i * 0.05:.2f}" for i in range(52)
    }
    # Normales Markdown-Format
    message = "🗓️ *Ergebnisse aller Wochen 2025*\n\n"
    for week, result in results.items():
        message += f"{week}: {result}%\n"
    await update.message.reply_text(message, parse_mode="Markdown", reply_markup=reply_markup)

async def yearly(update, context):
    # Definiere Custom Keyboard
    keyboard = [
        ["ℹ️ Informationen", "📈 Heutiges Ergebnis"],
        ["📅 Ergebnisse (Aktuelle Woche)", "🗓️ Ergebnisse (Aktueller Monat)"],
        ["🗂️ Ergebnisse (Aktuelles Jahr)"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    # Simuliere Ergebnisse für das aktuelle Jahr (Platzhalter)
    results = [  # PLATZHALTER_YEARLY_RESULTS: Ersetze mit echten Daten
        ("2025", "1.50")
    ]
    # Normales Markdown-Format
    message = "🗂️ *Ergebnisse des Jahres*\n\n"
    for year, result in results:
        message += f"{year}: {result}%"
    await update.message.reply_text(message, parse_mode="Markdown", reply_markup=reply_markup)

async def handle_keyboard_buttons(update, context):
    # Abfangen der Custom Keyboard Button-Interaktionen
    text = update.message.text
    # Definiere Custom Keyboard
    keyboard = [
        ["ℹ️ Informationen", "📈 Heutiges Ergebnis"],
        ["📅 Ergebnisse (Aktuelle Woche)", "🗓️ Ergebnisse (Aktueller Monat)"],
        ["🗂️ Ergebnisse (Aktuelles Jahr)"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    if text == "ℹ️ Informationen":
        await info(update, context)
    elif text == "📈 Heutiges Ergebnis":
        await result(update, context)
    elif text == "📅 Ergebnisse (Aktuelle Woche)":
        await daily(update, context)
    elif text == "🗓️ Ergebnisse (Aktueller Monat)":
        await weekly(update, context)
    elif text == "🗂️ Ergebnisse (Aktuelles Jahr)":
        await yearly(update, context)
    else:
        await update.message.reply_text(
            "Bitte wähle einen Befehl aus der Tastatur.",
            reply_markup=reply_markup
        )

async def button_callback(update, context):
    query = update.callback_query
    await query.answer(text=f"Du hast {query.data.replace('cmd_', '')} gewählt!")  # Bestätigungsmeldung
    # Definiere Custom Keyboard für Inline-Button-Antworten
    keyboard = [
        ["ℹ️ Informationen", "📈 Heutiges Ergebnis"],
        ["📅 Ergebnisse (Aktuelle Woche)", "🗓️ Ergebnisse (Aktueller Monat)"],
        ["🗂️ Ergebnisse (Aktuelles Jahr)"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    if query.data == "cmd_info":
        await query.message.reply_text(
            "ℹ️ *Info*\n"
            "Dies ist ein Platzhaltertext für den Bot. Er beschreibt, worum es geht. "
            "#PLATZHALTER_INFO_TEXT",  # Platzhalter für späteren Info-Text
            parse_mode="Markdown",
            reply_markup=reply_markup
        )
    elif query.data == "cmd_result":
        result_percent = "1.04"  # PLATZHALTER_RESULT_PERCENT: Ersetze mit echtem Wert
        today = datetime.now().strftime("%Y-%m-%d")  # Aktuelles Datum
        await query.message.reply_text(
            f"📈 *Das Ergebnis von heute {today}*\n"
            f"{result_percent}%",
            parse_mode="Markdown",
            reply_markup=reply_markup
        )
    elif query.data == "cmd_daily":
        today = datetime.now()
        week_start = today - timedelta(days=today.weekday())
        results = {  # PLATZHALTER_DAILY_RESULTS: Ersetze mit echten Daten
            (week_start + timedelta(days=i)).strftime("%Y-%m-%d"): f"{1.00 + i * 0.1:.2f}"
            for i in range(7)
        }
        message = "📅 *Ergebnisse der aktuellen Woche*\n\n"
        for date, result in results.items():
            message += f"{date}: {result}%\n"
        await query.message.reply_text(message, parse_mode="Markdown", reply_markup=reply_markup)
    elif query.data == "cmd_weekly":
        results = {  # PLATZHALTER_WEEKLY_RESULTS: Ersetze mit echten Daten
            f"Woche {i+1}": f"{1.00 + i * 0.05:.2f}" for i in range(52)
        }
        message = "🗓️ *Ergebnisse aller Wochen 2025*\n\n"
        for week, result in results.items():
            message += f"{week}: {result}%\n"
        await query.message.reply_text(message, parse_mode="Markdown", reply_markup=reply_markup)
    elif query.data == "cmd_yearly":
        results = [  # PLATZHALTER_YEARLY_RESULTS: Ersetze mit echten Daten
            ("2025", "1.50")
        ]
        message = "🗂️ *Ergebnisse des Jahres*\n\n"
        for year, result in results:
            message += f"{year}: {result}%"
        await query.message.reply_text(message, parse_mode="Markdown", reply_markup=reply_markup)

def main():
    # Erstelle die Application
    app = Application.builder().token(TOKEN).build()

    # Füge Befehle hinzu
    app.add_handler(CommandHandler("dashboard", dashboard))
    app.add_handler(CommandHandler("info", info))
    app.add_handler(CommandHandler("result", result))
    app.add_handler(CommandHandler("daily", daily))
    app.add_handler(CommandHandler("weekly", weekly))
    app.add_handler(CommandHandler("yearly", yearly))
    app.add_handler(CallbackQueryHandler(button_callback))
    # Füge MessageHandler für Custom Keyboard Buttons hinzu
    app.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_keyboard_buttons))

    # Starte Webhook (kein set_my_commands, um linken Menü-Button zu entfernen)
    app.run_webhook(
        listen="0.0.0.0",
        port=int(os.getenv("PORT", 8443)),
        url_path=TOKEN,
        webhook_url=f"https://{os.getenv('RENDER_EXTERNAL_HOSTNAME')}/{TOKEN}"
    )

if __name__ == "__main__":
    main()