from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import filters
import os
from datetime import datetime, timedelta

# Bot-Token aus Umgebungsvariablen
TOKEN = os.getenv("TELEGRAM_TOKEN")

async def start(update, context):
    # Definiere Custom Keyboard
    keyboard = [
        ["ℹ️ Info", "📈 Letztes Ergebnis"],
        ["📅 Ergebnisse (Aktuelle Woche)", "🗓️ Ergebnisse (Monate)"],
        ["🗂️ Ergebnisse (Aktuelles Jahr)"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    message = (
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
    await update.message.reply_text(message, reply_markup=reply_markup, parse_mode="Markdown")

async def dashboard(update, context):
    # Definiere Custom Keyboard
    keyboard = [
        ["ℹ️ Info", "📈 Letztes Ergebnis"],
        ["📅 Ergebnisse (Aktuelle Woche)", "🗓️ Ergebnisse (Monate)"],
        ["🗂️ Ergebnisse (Aktuelles Jahr)"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    message = (
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
    await update.message.reply_text(message, reply_markup=reply_markup, parse_mode="Markdown")

async def info(update, context):
    # Definiere Custom Keyboard
    keyboard = [
        ["ℹ️ Info", "📈 Letztes Ergebnis"],
        ["📅 Ergebnisse (Aktuelle Woche)", "🗓️ Ergebnisse (Monate)"],
        ["🗂️ Ergebnisse (Aktuelles Jahr)"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    message = (
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
    await update.message.reply_text(message, reply_markup=reply_markup, parse_mode="Markdown")

async def result(update, context):
    # Definiere Custom Keyboard
    keyboard = [
        ["ℹ️ Info", "📈 Letztes Ergebnis"],
        ["📅 Ergebnisse (Aktuelle Woche)", "🗓️ Ergebnisse (Monate)"],
        ["🗂️ Ergebnisse (Aktuelles Jahr)"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    result_percent = "1.04"  # PLATZHALTER_RESULT_PERCENT: Ersetze mit echtem Wert
    today = datetime.now().strftime("%d.%m.%Y")  # Aktuelles Datum im Format DD.MM.YYYY
    await update.message.reply_text(
        f"📈 *Letztes Ergebnis vom {today}*\n\n"
        f"✅ {result_percent}%",
        parse_mode="Markdown",
        reply_markup=reply_markup
    )

async def daily(update, context):
    # Definiere Custom Keyboard
    keyboard = [
        ["ℹ️ Info", "📈 Letztes Ergebnis"],
        ["📅 Ergebnisse (Aktuelle Woche)", "🗓️ Ergebnisse (Monate)"],
        ["🗂️ Ergebnisse (Aktuelles Jahr)"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    # Simuliere Ergebnisse für die aktuelle Woche, nur Werktage (Platzhalter)
    today = datetime.now()
    week_start = today - timedelta(days=today.weekday())
    weekdays = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag"]
    results = {  # PLATZHALTER_DAILY_RESULTS: Ersetze mit echten Daten
        (week_start + timedelta(days=i)).strftime("%d.%m.%Y"): f"{1.00 + i * 0.1:.2f}"
        for i in range(5)  # Nur Montag bis Freitag
    }
    # Normales Markdown-Format
    message = "📅 *Ergebnisse der aktuellen Woche*\n\n"
    for i, (date, result) in enumerate(results.items()):
        message += f"{date}, {weekdays[i]}: {result}%\n"
    await update.message.reply_text(message, parse_mode="Markdown", reply_markup=reply_markup)

async def weekly(update, context):
    # Definiere Custom Keyboard
    keyboard = [
        ["ℹ️ Info", "📈 Letztes Ergebnis"],
        ["📅 Ergebnisse (Aktuelle Woche)", "🗓️ Ergebnisse (Monate)"],
        ["🗂️ Ergebnisse (Aktuelles Jahr)"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    # Simuliere Ergebnisse für Wochen bis zur aktuellen Woche (Platzhalter)
    today = datetime.now()
    current_week = today.isocalendar().week  # Aktuelle Woche (z. B. 35 für 31.08.2025)
    results = {  # PLATZHALTER_WEEKLY_RESULTS: Ersetze mit echten Daten
        f"Woche {i+1}": f"{1.00 + i * 0.05:.2f}" for i in range(current_week)
    }
    # Normales Markdown-Format
    message = "🗓️ *Ergebnisse (Monate)*\n\n"
    for week, result in results.items():
        message += f"{week}: {result}%\n"
    await update.message.reply_text(message, parse_mode="Markdown", reply_markup=reply_markup)

async def yearly(update, context):
    # Definiere Custom Keyboard
    keyboard = [
        ["ℹ️ Info", "📈 Letztes Ergebnis"],
        ["📅 Ergebnisse (Aktuelle Woche)", "🗓️ Ergebnisse (Monate)"],
        ["🗂️ Ergebnisse (Aktuelles Jahr)"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    # Simuliere Ergebnisse für das aktuelle Jahr (Platzhalter)
    results = [  # PLATZHALTER_YEARLY_RESULTS: Ersetze mit echten Daten
        ("2025", "1.50")
    ]
    # Normales Markdown-Format
    message = "🗂️ *Ergebnisse (Jahre)*\n\n"
    for year, result in results:
        message += f"{year}: {result}%"
    await update.message.reply_text(message, parse_mode="Markdown", reply_markup=reply_markup)

async def handle_keyboard_buttons(update, context):
    # Abfangen der Custom Keyboard Button-Interaktionen
    text = update.message.text
    # Definiere Custom Keyboard
    keyboard = [
        ["ℹ️ Info", "📈 Letztes Ergebnis"],
        ["📅 Ergebnisse (Aktuelle Woche)", "🗓️ Ergebnisse (Monate)"],
        ["🗂️ Ergebnisse (Aktuelles Jahr)"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
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
            reply_markup=reply_markup
        )

async def button_callback(update, context):
    query = update.callback_query
    await query.answer(text=f"Du hast {query.data.replace('cmd_', '')} gewählt!")  # Bestätigungsmeldung
    # Definiere Custom Keyboard für Inline-Button-Antworten
    keyboard = [
        ["ℹ️ Info", "📈 Letztes Ergebnis"],
        ["📅 Ergebnisse (Aktuelle Woche)", "🗓️ Ergebnisse (Monate)"],
        ["🗂️ Ergebnisse (Aktuelles Jahr)"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    if query.data == "cmd_info":
        message = (
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
        await query.message.reply_text(message, reply_markup=reply_markup, parse_mode="Markdown")
    elif query.data == "cmd_result":
        result_percent = "1.04"  # PLATZHALTER_RESULT_PERCENT: Ersetze mit echtem Wert
        today = datetime.now().strftime("%d.%m.%Y")  # Aktuelles Datum im Format DD.MM.YYYY
        await query.message.reply_text(
            f"📈 *Letztes Ergebnis vom {today}*\n\n"
            f"✅ {result_percent}%",
            parse_mode="Markdown",
            reply_markup=reply_markup
        )
    elif query.data == "cmd_daily":
        today = datetime.now()
        week_start = today - timedelta(days=today.weekday())
        weekdays = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag"]
        results = {  # PLATZHALTER_DAILY_RESULTS: Ersetze mit echten Daten
            (week_start + timedelta(days=i)).strftime("%d.%m.%Y"): f"{1.00 + i * 0.1:.2f}"
            for i in range(5)  # Nur Montag bis Freitag
        }
        message = "📅 *Ergebnisse der aktuellen Woche*\n\n"
        for i, (date, result) in enumerate(results.items()):
            message += f"{date}, {weekdays[i]}: {result}%\n"
        await query.message.reply_text(message, parse_mode="Markdown", reply_markup=reply_markup)
    elif query.data == "cmd_weekly":
        today = datetime.now()
        current_week = today.isocalendar().week  # Aktuelle Woche
        results = {  # PLATZHALTER_WEEKLY_RESULTS: Ersetze mit echten Daten
            f"Woche {i+1}": f"{1.00 + i * 0.05:.2f}" for i in range(current_week)
        }
        message = "🗓️ *Ergebnisse (Monate)*\n\n"
        for week, result in results.items():
            message += f"{week}: {result}%\n"
        await query.message.reply_text(message, parse_mode="Markdown", reply_markup=reply_markup)
    elif query.data == "cmd_yearly":
        results = [  # PLATZHALTER_YEARLY_RESULTS: Ersetze mit echten Daten
            ("2025", "1.50")
        ]
        message = "🗂️ *Ergebnisse (Jahre)*\n\n"
        for year, result in results:
            message += f"{year}: {result}%"
        await query.message.reply_text(message, parse_mode="Markdown", reply_markup=reply_markup)

def main():
    # Erstelle die Application
    app = Application.builder().token(TOKEN).build()

    # Füge Befehle hinzu
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("dashboard", dashboard))
    app.add_handler(CommandHandler("info", info))
    app.add_handler(CommandHandler("result", result))
    app.add_handler(CommandHandler("daily", daily))
    app.add_handler(CommandHandler("weekly", weekly))
    app.add_handler(CommandHandler("yearly", yearly))
    app.add_handler(CallbackQueryHandler(button_callback))
    # Füge MessageHandler für Custom Keyboard Buttons hinzu
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_keyboard_buttons))

    # Starte Webhook (kein set_my_commands, um linken Menü-Button zu entfernen)
    app.run_webhook(
        listen="0.0.0.0",
        port=int(os.getenv("PORT", 8443)),
        url_path=TOKEN,
        webhook_url=f"https://{os.getenv('RENDER_EXTERNAL_HOSTNAME')}/{TOKEN}"
    )

if __name__ == "__main__":
    main()