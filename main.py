import os
import requests
from datetime import datetime, timedelta
from telegram import ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters

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

async def fetch_airtable_data(context, year):
    """Holt Daten aus Airtable für ein gegebenes Jahr und speichert sie im Cache."""
    cache_key = f"airtable_cache_{year}"
    timestamp_key = f"cache_timestamp_{year}"
    # Prüfe Cache (5 Minuten Gültigkeit)
    if cache_key in context.bot_data and timestamp_key in context.bot_data:
        if (datetime.now() - context.bot_data[timestamp_key]).seconds < 300:
            return context.bot_data[cache_key]
    
    headers = {"Authorization": f"Bearer {os.getenv('AIRTABLE_TOKEN')}"}
    base_id = os.getenv(f"AIRTABLE_BASE_{year}")
    table_id = os.getenv(f"AIRTABLE_TBL_{year}")
    records = []
    params = {"sort[0][field]": "Date", "sort[0][direction]": "desc"}
    
    try:
        while True:
            response = requests.get(
                f"https://api.airtable.com/v0/{base_id}/{table_id}",
                headers=headers,
                params=params
            )
            response.raise_for_status()  # Fehler bei nicht-200 Status
            data = response.json()
            records.extend([
                {"Date": r["fields"]["Date"], "Result": r["fields"]["Result"]}
                for r in data.get("records", []) if "Date" in r["fields"] and "Result" in r["fields"]
            ])
            if "offset" not in data:
                break
            params["offset"] = data["offset"]
    except requests.RequestException as e:
        # Fallback auf Cache bei API-Fehler
        return context.bot_data.get(cache_key, [])
    
    context.bot_data[cache_key] = records
    context.bot_data[timestamp_key] = datetime.now()
    return records

async def get_all_data(context):
    """Kombiniert Daten aus allen Jahren."""
    data = []
    for year in ["2023", "2024", "2025"]:
        data.extend(await fetch_airtable_data(context, year))
    return data

async def start(update, context):
    await update.message.reply_text(DASHBOARD_MESSAGE, reply_markup=KEYBOARD, parse_mode="Markdown")

async def dashboard(update, context):
    await update.message.reply_text(DASHBOARD_MESSAGE, reply_markup=KEYBOARD, parse_mode="Markdown")

async def info(update, context):
    await update.message.reply_text(DASHBOARD_MESSAGE, reply_markup=KEYBOARD, parse_mode="Markdown")

async def result(update, context):
    data = await get_all_data(context)
    if not data:
        await update.message.reply_text("Keine Daten verfügbar.", reply_markup=KEYBOARD)
        return
    latest = max(data, key=lambda x: datetime.strptime(x["Date"], "%d.%m.%Y"))
    message = f"📈 *Letztes Ergebnis vom {latest['Date']}*\n\n✅ {latest['Result']}%"
    await update.message.reply_text(message, reply_markup=KEYBOARD, parse_mode="Markdown")

async def daily(update, context):
    data = await get_all_data(context)
    today = datetime.now()
    week_start = today - timedelta(days=today.weekday())
    week_end = week_start + timedelta(days=4)  # Freitag
    week_data = [
        r for r in data
        if week_start.date() <= datetime.strptime(r["Date"], "%d.%m.%Y").date() <= week_end.date()
    ]
    message = "📅 *Ergebnisse der aktuellen Woche*\n\n"
    if week_data:
        for r in sorted(week_data, key=lambda x: datetime.strptime(x["Date"], "%d.%m.%Y")):
            date_obj = datetime.strptime(r["Date"], "%d.%m.%Y")
            weekday = WEEKDAYS[date_obj.weekday()]
            message += f"{r['Date']}, {weekday}: {r['Result']}%\n"
    else:
        message += "Keine Ergebnisse für die aktuelle Woche.\n"
    await update.message.reply_text(message, reply_markup=KEYBOARD, parse_mode="Markdown")

async def weekly(update, context):
    data = await get_all_data(context)
    today = datetime.now()
    current_week = today.isocalendar().week
    message = "🗓️ *Ergebnisse (Monate)*\n\n"
    if data:
        weekly_results = {}
        for r in data:
            date_obj = datetime.strptime(r["Date"], "%d.%m.%Y")
            year_week = (date_obj.year, date_obj.isocalendar().week)
            if year_week not in weekly_results:
                weekly_results[year_week] = []
            weekly_results[year_week].append(r["Result"])
        for (year, week), results in sorted(weekly_results.items()):
            if year == today.year and week > current_week:
                continue
            avg = sum(results) / len(results) if results else 0
            message += f"Woche {week} ({year}): {avg:.2f}%\n"
    else:
        message += "Keine Ergebnisse verfügbar.\n"
    await update.message.reply_text(message, reply_markup=KEYBOARD, parse_mode="Markdown")

async def yearly(update, context):
    data = await get_all_data(context)
    message = "🗂️ *Ergebnisse (Jahre)*\n\n"
    if data:
        yearly_results = {}
        for r in data:
            year = datetime.strptime(r["Date"], "%d.%m.%Y").year
            if year not in yearly_results:
                yearly_results[year] = []
            yearly_results[year].append(r["Result"])
        for year in sorted(yearly_results.keys()):
            avg = sum(yearly_results[year]) / len(yearly_results[year]) if yearly_results[year] else 0
            message += f"{year}: {avg:.2f}%"
    else:
        message += "Keine Ergebnisse verfügbar.\n"
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
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("dashboard", dashboard))
    app.add_handler(CommandHandler("info", info))
    app.add_handler(CommandHandler("result", result))
    app.add_handler(CommandHandler("daily", daily))
    app.add_handler(CommandHandler("weekly", weekly))
    app.add_handler(CommandHandler("yearly", yearly))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_keyboard_buttons))
    app.run_webhook(
        listen="0.0.0.0",
        port=int(os.getenv("PORT", 8443)),
        url_path=TOKEN,
        webhook_url=f"https://{os.getenv('RENDER_EXTERNAL_HOSTNAME')}/{TOKEN}"
    )

if __name__ == "__main__":
    main()