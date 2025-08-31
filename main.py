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
        ["ℹ️ Info", "📈 Heutiges Ergebnis"],
        ["📅 Ergebnisse (Aktuelle Woche)", "🗓️ Ergebnisse (Monate)"],
        ["🗂️ Ergebnisse (Aktuelles Jahr)"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    message = (
        "*📊 Dein Bot-Dashboard 📊*\n"
        "Wähle einen Befehl aus:\n\n"
        "ℹ️ *Info*: Zeigt Infos zum Bot (/info)\n"
        "📈 *Result*: Zeigt das heutige Ergebnis (/result)\n"
        "📅 *Daily*: Ergebnisse dieser Woche (/daily)\n"
        "🗓️ *Weekly*: Ergebnisse aller Wochen (/weekly)\n"
        "🗂️ *Yearly*: Ergebnisse des Jahres (/yearly)\n\n"
        "Bitte wähle einen Befehl aus dem unteren Menü."
    )
    await update.message.reply_text(message, reply_markup=reply_markup, parse_mode="Markdown")

async def dashboard(update, context):
    # Definiere Custom Keyboard
    keyboard = [
        ["ℹ️ Info", "📈 Heutiges Ergebnis"],
        ["📅 Ergebnisse (Aktuelle Woche)", "🗓️ Ergebnisse (Monate)"],
        ["🗂️ Ergebnisse (Aktuelles Jahr)"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    message = (
        "*📊 Dein Bot-Dashboard 📊*\n"
        "Wähle einen Befehl aus:\n\n"
        "ℹ️ *Info*: Zeigt Infos zum Bot (/info)\n"
        "📈 *Result*: Zeigt das heutige Ergebnis (/result)\n"
        "📅 *Daily*: Ergebnisse dieser Woche (/daily)\n"
        "🗓️ *Weekly*: Ergebnisse aller Wochen (/weekly)\n"
        "🗂️ *Yearly*: Ergebnisse des Jahres (/yearly)\n\n"
        "Bitte wähle einen Befehl aus dem unteren Menü."
    )
    await update.message.reply_text(message, reply_markup=reply_markup, parse_mode="Markdown")

async def info(update, context):
    # Definiere Custom Keyboard
    keyboard = [
        ["ℹ️ Info", "📈 Heutiges Ergebnis"],
        ["📅 Ergebnisse (Aktuelle Woche)", "🗓️ Ergebnisse (Monate)"],
        ["🗂️ Ergebnisse (Aktuelles Jahr)"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    message = (
        "*📊 Dein Bot-Dashboard 📊*\n"
        "Wähle einen Befehl aus:\n\n"
        "ℹ️ *Info*: Zeigt Infos zum Bot (/info)\n"
        "📈 *Result*: Zeigt das heutige Ergebnis (/result)\n"
        "📅 *Daily*: Ergebnisse dieser Woche (/daily)\n"
        "🗓️ *Weekly*: Ergebnisse aller Wochen (/weekly)\n"
        "🗂️ *Yearly*: Ergebnisse des Jahres (/yearly)\n\n"
        "Bitte wähle einen Befehl aus dem unteren Menü."
    )
    await update.message.reply_text(message, reply_markup=reply_markup, parse_mode="Markdown")

async def result(update, context):
    # Definiere Custom Keyboard
    keyboard = [
        ["ℹ️ Info", "📈 Heutiges Ergebnis"],
        ["📅 Ergebnisse (Aktuelle Woche)", "🗓️ Ergebnisse (Monate)"],
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
        ["ℹ️ Info", "📈 Heutiges Ergebnis"],
        ["📅 Ergebnisse (Aktuelle Woche)", "🗓️ Ergebnisse (Monate)"],
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
        ["ℹ️ Info", "📈 Heutiges Ergebnis"],
        ["📅 Ergebnisse (Aktuelle Woche)", "🗓️ Ergebnisse (Monate)"],
        ["🗂️ Ergebnisse (Aktuelles Jahr)"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    # Setze Wochen-Offset auf 0 für /weekly
    context.user_data['week_offset'] = 0
    # Simuliere Ergebnisse für 52 Wochen (Platzhalter)
    results = {  # PLATZHALTER_WEEKLY_RESULTS: Ersetze mit echten Daten
        f"Woche {i+1}": f"{1.00 + i * 0.05:.2f}" for i in range(52)
    }
    # Zeige nur 4 Wochen an
    start_week = context.user_data['week_offset']
    end_week = start_week + 4
    message = "🗓️ *Ergebnisse (Monate)*\n\n"
    for week, result in list(results.items())[start_week:end_week]:
        message += f"{week}: {result}%\n"
    message += "\nVerwende /next, um die nächsten Wochen anzuzeigen."
    await update.message.reply_text(message, parse_mode="Markdown", reply_markup=reply_markup)

async def next(update, context):
    # Definiere Custom Keyboard
    keyboard = [
        ["ℹ️ Info", "📈 Heutiges Ergebnis"],
        ["📅 Ergebnisse (Aktuelle Woche)", "🗓️ Ergebnisse (Monate)"],
        ["🗂️ Ergebnisse (Aktuelles Jahr)"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    # Erhöhe Wochen-Offset um 4
    context.user_data['week_offset'] = context.user_data.get('week_offset', 0) + 4
    # Simuliere Ergebnisse für 52 Wochen (Platzhalter)
    results = {  # PLATZHALTER_WEEKLY_RESULTS: Ersetze mit echten Daten
        f"Woche {i+1}": f"{1.00 + i * 0.05:.2f}" for i in range(52)
    }
    # Zeige nur 4 Wochen an
    start_week = context.user_data['week_offset']
    end_week = start_week + 4
    if start_week >= len(results):
        context.user_data['week_offset'] = 0  # Zurücksetzen, wenn Ende erreicht
        start_week = 0
        end_week = 4
        message = "🗓️ *Ergebnisse (Monate)*\n\nZurück zu den ersten Wochen:\n\n"
    else:
        message = "🗓️ *Ergebnisse (Monate)*\n\n"
    for week, result in list(results.items())[start_week:end_week]:
        message += f"{week}: {result}%\n"
    message += "\nVerwende /next, um die nächsten Wochen anzuzeigen."
    await update.message.reply_text(message, parse_mode="Markdown", reply_markup=reply_markup)

async def yearly(update, context):
    # Definiere Custom Keyboard
    keyboard = [
        ["ℹ️ Info", "📈 Heutiges Ergebnis"],
        ["📅 Ergebnisse (Aktuelle Woche)", "🗓️ Ergebnisse (Monate)"],
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
        ["ℹ️ Info", "📈 Heutiges Ergebnis"],
        ["📅 Ergebnisse (Aktuelle Woche)", "🗓️ Ergebnisse (Monate)"],
        ["🗂️ Ergebnisse (Aktuelles Jahr)"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    if text == "ℹ️ Info":
        await info(update, context)
    elif text == "📈 Heutiges Ergebnis":
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
        ["ℹ️ Info", "📈 Heutiges Ergebnis"],
        ["📅 Ergebnisse (Aktuelle Woche)", "🗓️ Ergebnisse (Monate)"],
        ["🗂️ Ergebnisse (Aktuelles Jahr)"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    if query.data == "cmd_info":
        message = (
            "*📊 Dein Bot-Dashboard 📊*\n"
            "Wähle einen Befehl aus:\n\n"
            "ℹ️ *Info*: Zeigt Infos zum Bot (/info)\n"
            "📈 *Result*: Zeigt das heutige Ergebnis (/result)\n"
            "📅 *Daily*: Ergebnisse dieser Woche (/daily)\n"
            "🗓️ *Weekly*: Ergebnisse aller Wochen (/weekly)\n"
            "🗂️ *Yearly*: Ergebnisse des Jahres (/yearly)\n\n"
            "Bitte wähle einen Befehl aus dem unteren Menü."
        )
        await query.message.reply_text(message, reply_markup=reply_markup, parse_mode="Markdown")
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
        # Setze Wochen-Offset auf 0 für cmd_weekly
        context.user_data['week_offset'] = 0
        results = {  # PLATZHALTER_WEEKLY_RESULTS: Ersetze mit echten Daten
            f"Woche {i+1}": f"{1.00 + i * 0.05:.2f}" for i in range(52)
        }
        start_week = context.user_data['week_offset']
        end_week = start_week + 4
        message = "🗓️ *Ergebnisse (Monate)*\n\n"
        for week, result in list(results.items())[start_week:end_week]:
            message += f"{week}: {result}%\n"
        message += "\nVerwende /next, um die nächsten Wochen anzuzeigen."
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
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("dashboard", dashboard))
    app.add_handler(CommandHandler("info", info))
    app.add_handler(CommandHandler("result", result))
    app.add_handler(CommandHandler("daily", daily))
    app.add_handler(CommandHandler("weekly", weekly))
    app.add_handler(CommandHandler("next", next))
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