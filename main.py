from telegram.ext import Application, CommandHandler, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import os
from datetime import datetime, timedelta

# Bot-Token aus Umgebungsvariablen
TOKEN = os.getenv("TELEGRAM_TOKEN")

async def dashboard(update, context):
    # Definiere Buttons mit Emojis (ohne /dashboard)
    keyboard = [
        [  # Erste Reihe
            InlineKeyboardButton("ℹ️ Info", callback_data="cmd_info"),
            InlineKeyboardButton("📈 Result", callback_data="cmd_result"),
        ],
        [  # Zweite Reihe
            InlineKeyboardButton("📅 Daily", callback_data="cmd_daily"),
            InlineKeyboardButton("🗓️ Weekly", callback_data="cmd_weekly"),
        ],
        [  # Dritte Reihe
            InlineKeyboardButton("🗂️ Yearly", callback_data="cmd_yearly"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    # Formatiere die Nachricht mit Markdown
    message = (
        "*📊 Dein Bot-Dashboard 📊*\n"
        "Wähle einen Befehl aus:\n\n"
        "ℹ️ *Info*: Zeigt Infos zum Bot\n"
        "📈 *Result*: Zeigt das heutige Ergebnis\n"
        "📅 *Daily*: Ergebnisse dieser Woche\n"
        "🗓️ *Weekly*: Ergebnisse aller Wochen\n"
        "🗂️ *Yearly*: Ergebnisse des Jahres"
    )
    await update.message.reply_text(message, reply_markup=reply_markup, parse_mode="Markdown")

async def info(update, context):
    await update.message.reply_text(
        "ℹ️ *Info*\n"
        "Dies ist ein Platzhaltertext für den Bot. Er beschreibt, worum es geht. "
        "#PLATZHALTER_INFO_TEXT",  # Platzhalter für späteren Info-Text
        parse_mode="Markdown"
    )

async def result(update, context):
    result_percent = "1.00"  # PLATZHALTER_RESULT_PERCENT: Ersetze mit echtem Wert
    await update.message.reply_text(
        f"📈 *Das heutige Ergebnis beträgt* {result_percent} %",
        parse_mode="Markdown"
    )

async def daily(update, context):
    # Simuliere Ergebnisse für die aktuelle Woche (Platzhalter)
    today = datetime.now()
    week_start = today - timedelta(days=today.weekday())
    results = {  # PLATZHALTER_DAILY_RESULTS: Ersetze mit echten Daten
        (week_start + timedelta(days=i)).strftime("%Y-%m-%d"): f"{1.00 + i * 0.1:.2f}"
        for i in range(7)
    }
    # Konsolen-Format mit Markdown
    message = "📅 *Ergebnisse der aktuellen Woche*\n```\n"
    for date, result in results.items():
        message += f"{date}: {result} %\n"
    message += "```"
    await update.message.reply_text(message, parse_mode="Markdown")

async def weekly(update, context):
    # Simuliere Ergebnisse für 52 Wochen (Platzhalter)
    results = {  # PLATZHALTER_WEEKLY_RESULTS: Ersetze mit echten Daten
        f"Woche {i+1}": f"{1.00 + i * 0.05:.2f}" for i in range(52)
    }
    # Konsolen-Format mit Markdown
    message = "🗓️ *Ergebnisse aller Wochen 2025*\n```\n"
    for week, result in results.items():
        message += f"{week}: {result} %\n"
    message += "```"
    await update.message.reply_text(message, parse_mode="Markdown")

async def yearly(update, context):
    # Simuliere Ergebnisse für das aktuelle Jahr (Platzhalter)
    results = [  # PLATZHALTER_YEARLY_RESULTS: Ersetze mit echten Daten
        ("2025", "1.50")
    ]
    # Konsolen-Format mit Markdown
    message = "🗂️ *Ergebnisse des Jahres*\n```\n"
    for year, result in results:
        message += f"{year}: {result} %\n"
    message += "```"
    await update.message.reply_text(message, parse_mode="Markdown")

async def button_callback(update, context):
    query = update.callback_query
    await query.answer(text=f"Du hast {query.data.replace('cmd_', '')} gewählt!")  # Bestätigungsmeldung
    if query.data == "cmd_info":
        await query.message.reply_text(
            "ℹ️ *Info*\n"
            "Dies ist ein Platzhaltertext für den Bot. Er beschreibt, worum es geht. "
            "#PLATZHALTER_INFO_TEXT",  # Platzhalter für späteren Info-Text
            parse_mode="Markdown"
        )
    elif query.data == "cmd_result":
        result_percent = "1.00"  # PLATZHALTER_RESULT_PERCENT: Ersetze mit echtem Wert
        await query.message.reply_text(
            f"📈 *Das heutige Ergebnis beträgt* {result_percent} %",
            parse_mode="Markdown"
        )
    elif query.data == "cmd_daily":
        today = datetime.now()
        week_start = today - timedelta(days=today.weekday())
        results = {  # PLATZHALTER_DAILY_RESULTS: Ersetze mit echten Daten
            (week_start + timedelta(days=i)).strftime("%Y-%m-%d"): f"{1.00 + i * 0.1:.2f}"
            for i in range(7)
        }
        message = "📅 *Ergebnisse der aktuellen Woche*\n```\n"
        for date, result in results.items():
            message += f"{date}: {result} %\n"
        message += "```"
        await query.message.reply_text(message, parse_mode="Markdown")
    elif query.data == "cmd_weekly":
        results = {  # PLATZHALTER_WEEKLY_RESULTS: Ersetze mit echten Daten
            f"Woche {i+1}": f"{1.00 + i * 0.05:.2f}" for i in range(52)
        }
        message = "🗓️ *Ergebnisse aller Wochen 2025*\n```\n"
        for week, result in results.items():
            message += f"{week}: {result} %\n"
        message += "```"
        await query.message.reply_text(message, parse_mode="Markdown")
    elif query.data == "cmd_yearly":
        results = [  # PLATZHALTER_YEARLY_RESULTS: Ersetze mit echten Daten
            ("2025", "1.50")
        ]
        message = "🗂️ *Ergebnisse des Jahres*\n```\n"
        for year, result in results:
            message += f"{year}: {result} %\n"
        message += "```"
        await query.message.reply_text(message, parse_mode="Markdown")

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

    # Starte Webhook
    app.run_webhook(
        listen="0.0.0.0",
        port=int(os.getenv("PORT", 8443)),
        url_path=TOKEN,
        webhook_url=f"https://{os.getenv('RENDER_EXTERNAL_HOSTNAME')}/{TOKEN}"
    )

if __name__ == "__main__":
    main()