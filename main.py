import os
import requests
from datetime import datetime, timedelta
from telegram import ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from config import DATE_FORMAT, PERCENT_FORMAT, EMOJIS  # Importiere aus config.py

# Bot-Token aus Umgebungsvariablen
TOKEN = os.getenv("TELEGRAM_TOKEN")

# Globale Konstanten
KEYBOARD = ReplyKeyboardMarkup([
    ["ℹ️ Info", f"{EMOJIS['result']} Letztes Ergebnis"],
    [f"{EMOJIS['month']} Ergebnisse (Aktuelle Woche)", f"{EMOJIS['month']} Wochen (Aktueller Monat)"],
    [f"{EMOJIS['month']} Ergebnisse (Monate)", f"{EMOJIS['year']} Ergebnisse (Jahre)"]
], resize_keyboard=True)

WEEKDAYS = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag"]

DASHBOARD_MESSAGE = (
    f"*📊 Dein Bot-Dashboard 📊*\n\n"
    f"Willkommen im BE Bot Dashboard. Emojis: {EMOJIS['sum']} = Summen, {EMOJIS['month']} = Zeitbereiche, {EMOJIS['result']} = Einzelresultate\n\n"
    f"ℹ️ *Info*: Zeigt Infos zum Bot\n"
    f"Befehl: /info\n\n"
    f"{EMOJIS['result']} *Result*: Zeigt das letzte Ergebnis\n"
    f"Befehl: /result\n\n"
    f"{EMOJIS['month']} *Daily*: Ergebnisse der aktuellen Woche\n"
    f"Befehl: /daily\n\n"
    f"{EMOJIS['month']} *Weekly*: Ergebnisse der Wochen des aktuellen Monats\n"
    f"Befehl: /weekly\n\n"
    f"{EMOJIS['month']} *Monthly*: Ergebnisse aller Monate des aktuellen Jahres\n"
    f"Befehl: /monthly\n\n"
    f"{EMOJIS['year']} *Yearly*: Ergebnisse aller Jahre\n"
    f"Befehl: /yearly\n\n"
    f"{EMOJIS['refresh']} *Refresh*: Aktualisiert den Cache für aktuelle Daten (nur in Ausnahmefällen verwenden, z. B. bei aktualisierten Daten)\n"
    f"Befehl: /refresh\n\n"
    f"Bitte wähle einen Befehl aus dem unteren Menü."
)

def format_percent(value):
    """Formatiert einen Float- oder Integer-Wert als ###,##%."""
    return f"{float(value):{PERCENT_FORMAT}}%".replace(".", ",")

def get_week_date_range(week, year):
    """Gibt den Datumsbereich einer Woche (Montag bis Freitag) zurück."""
    first_day = datetime.strptime(f"{year}-W{week-1}-1", "%Y-W%W-%w")
    last_day = first_day + timedelta(days=4)  # Freitag
    return first_day.strftime(DATE_FORMAT), last_day.strftime(DATE_FORMAT)

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
    if not base_id or not table_id:
        return []
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
            for r in data.get("records", []):
                if "Date" not in r["fields"] or "Result" not in r["fields"]:
                    continue
                date_str = r["fields"]["Date"]
                try:
                    datetime.strptime(date_str, "%Y-%m-%d")
                    records.append({"Date": date_str, "Result": r["fields"]["Result"]})
                except ValueError:
                    try:
                        datetime.strptime(date_str, DATE_FORMAT)
                        date_obj = datetime.strptime(date_str, DATE_FORMAT)
                        records.append({"Date": date_obj.strftime("%Y-%m-%d"), "Result": r["fields"]["Result"]})
                    except ValueError:
                        continue
            if "offset" not in data:
                break
            params["offset"] = data["offset"]
    except requests.RequestException as e:
        print(f"Error fetching Airtable data for {year}: {e}")
        return context.bot_data.get(cache_key, [])  # Fallback auf Cache
    
    context.bot_data[cache_key] = records
    context.bot_data[timestamp_key] = datetime.now()
    return records

async def get_all_data(context):
    """Kombiniert Daten aus allen Jahren."""
    data = []
    for year in ["2023", "2024", "2025"]:
        data.extend(await fetch_airtable_data(context, year))
    return data

async def get_current_year_data(context):
    """Holt Daten nur für das aktuelle Jahr (2025)."""
    return await fetch_airtable_data(context, "2025")

async def start(update, context):
    await update.message.reply_text(DASHBOARD_MESSAGE, reply_markup=KEYBOARD, parse_mode="Markdown")

async def dashboard(update, context):
    await update.message.reply_text(DASHBOARD_MESSAGE, reply_markup=KEYBOARD, parse_mode="Markdown")

async def info(update, context):
    await update.message.reply_text(DASHBOARD_MESSAGE, reply_markup=KEYBOARD, parse_mode="Markdown")

async def refresh(update, context):
    today = datetime.now()
    year = str(today.year)
    cache_key = f"airtable_cache_{year}"
    timestamp_key = f"cache_timestamp_{year}"
    if cache_key in context.bot_data:
        del context.bot_data[cache_key]
    if timestamp_key in context.bot_data:
        del context.bot_data[timestamp_key]
    await update.message.reply_text(
        f"{EMOJIS['refresh']} Cache wurde aktualisiert. Bitte sende den gewünschten Befehl erneut.",
        reply_markup=KEYBOARD,
        parse_mode="Markdown"
    )

async def result(update, context):
    data = await get_current_year_data(context)
    if not data:
        await update.message.reply_text(
            f"Hoppla, die Daten konnten nicht geladen werden. Bitte versuche {EMOJIS['refresh']} /refresh oder später erneut.",
            reply_markup=KEYBOARD,
            parse_mode="Markdown"
        )
        return
    try:
        latest = max(data, key=lambda x: datetime.strptime(x["Date"], "%Y-%m-%d"))
        display_date = datetime.strptime(latest["Date"], "%Y-%m-%d").strftime(DATE_FORMAT)
        message = f"{EMOJIS['result']} *Letztes Ergebnis*\n\n{display_date}: {EMOJIS['result']} {format_percent(latest['Result'])}"
    except (ValueError, KeyError) as e:
        print(f"Error in /result: {e}")
        message = f"Hoppla, die Daten konnten nicht geladen werden. Bitte versuche {EMOJIS['refresh']} /refresh oder später erneut."
    await update.message.reply_text(message, reply_markup=KEYBOARD, parse_mode="Markdown")

async def daily(update, context):
    data = await get_current_year_data(context)
    today = datetime.now()
    week_start = today - timedelta(days=today.weekday())
    week_end = week_start + timedelta(days=4)  # Freitag
    week_data = [
        r for r in data
        if week_start.date() <= datetime.strptime(r["Date"], "%Y-%m-%d").date() <= week_end.date()
    ]
    week_num = today.isocalendar().week
    message = f"{EMOJIS['month']} *Ergebnisse der aktuellen Woche (KW {week_num} {today.year})*\n\n"
    if week_data:
        for r in sorted(week_data, key=lambda x: datetime.strptime(x["Date"], "%Y-%m-%d")):
            date_obj = datetime.strptime(r["Date"], "%Y-%m-%d")
            weekday = WEEKDAYS[date_obj.weekday()]
            display_date = date_obj.strftime(DATE_FORMAT)
            message += f"{display_date}, {weekday}: {format_percent(r['Result'])}\n"
        # Kumuliertes Ergebnis (Summe)
        total = sum(r["Result"] for r in week_data) if week_data else 0
        message += f"\n{EMOJIS['sum']} *Wochenergebnis*: {format_percent(total)}"
    else:
        message += f"Keine Ergebnisse für die aktuelle Woche.\n\n{EMOJIS['refresh']} Versuche /refresh, falls Daten fehlen."
    await update.message.reply_text(message, reply_markup=KEYBOARD, parse_mode="Markdown")

async def weekly(update, context):
    data = await get_current_year_data(context)
    today = datetime.now()
    current_month = today.month
    month_names = [
        "Januar", "Februar", "März", "April", "Mai", "Juni",
        "Juli", "August", "September", "Oktober", "November", "Dezember"
    ]
    month_name = month_names[current_month - 1]
    message = f"{EMOJIS['month']} *Ergebnisse des aktuellen Monats ({month_name} {today.year})*\n\n"
    if data:
        weekly_results = {}
        for r in data:
            try:
                date_obj = datetime.strptime(r["Date"], "%Y-%m-%d")
                if date_obj.year != today.year or date_obj.month != current_month:
                    continue
                week = date_obj.isocalendar().week
                if week not in weekly_results:
                    weekly_results[week] = []
                weekly_results[week].append(r["Result"])
            except ValueError:
                continue
        if weekly_results:
            for week in sorted(weekly_results.keys()):
                total = sum(weekly_results[week]) if weekly_results[week] else 0
                start_date, end_date = get_week_date_range(week, today.year)
                message += f"*KW {week}*\n{start_date} - {end_date}: {EMOJIS['week']} {format_percent(total)}\n\n"
            # Monatsergebnis (Summe aller Ergebnisse im Monat)
            month_results = [r for w in weekly_results.values() for r in w]
            month_total = sum(month_results) if month_results else 0
            message += f"{EMOJIS['sum']} *Monatsergebnis*: {format_percent(month_total)}\n\n\n"
        else:
            message += f"Keine Ergebnisse für den aktuellen Monat.\n\n{EMOJIS['refresh']} Versuche /refresh, falls Daten fehlen."
    else:
        message += f"Keine Daten verfügbar.\n\n{EMOJIS['refresh']} Versuche /refresh, falls Daten fehlen."
    await update.message.reply_text(message, reply_markup=KEYBOARD, parse_mode="Markdown")

async def monthly(update, context):
    data = await get_current_year_data(context)
    today = datetime.now()
    message = f"{EMOJIS['month']} *Ergebnisse des aktuellen Jahres ({today.year})*\n\n"
    if data:
        monthly_results = {}
        month_names = [
            "Januar", "Februar", "März", "April", "Mai", "Juni",
            "Juli", "August", "September", "Oktober", "November", "Dezember"
        ]
        for r in data:
            try:
                date_obj = datetime.strptime(r["Date"], "%Y-%m-%d")
                if date_obj.year != today.year:
                    continue
                month = date_obj.month
                if month not in monthly_results:
                    monthly_results[month] = []
                monthly_results[month].append(r["Result"])
            except ValueError:
                continue
        for month in sorted(monthly_results.keys()):
            if month > today.month:
                continue
            total = sum(monthly_results[month]) if monthly_results[month] else 0
            month_name = month_names[month - 1]
            message += f"{EMOJIS['month']} {month_name} {today.year}: {format_percent(total)}\n\n"
        # Jahresergebnis (Summe aller Monate)
        year_results = [r for m in monthly_results.values() for r in m]
        year_total = sum(year_results) if year_results else 0
        message += f"{EMOJIS['sum']} *Jahresergebnis*: {format_percent(year_total)}"
    else:
        message += f"Keine Daten verfügbar.\n\n{EMOJIS['refresh']} Versuche /refresh, falls Daten fehlen."
    await update.message.reply_text(message, reply_markup=KEYBOARD, parse_mode="Markdown")

async def yearly(update, context):
    data = await get_all_data(context)
    message = f"{EMOJIS['year']} *Ergebnisse aller Jahre*\n\n"
    if data:
        yearly_results = {}
        for r in data:
            try:
                year = datetime.strptime(r["Date"], "%Y-%m-%d").year
                if year not in yearly_results:
                    yearly_results[year] = []
                yearly_results[year].append(r["Result"])
            except ValueError:
                continue
        for year in sorted(yearly_results.keys()):
            total = sum(yearly_results[year]) if yearly_results[year] else 0
            message += f"{EMOJIS['year']} {year}: {format_percent(total)}\n\n"
        # Gesamtergebnis (Summe aller Jahre)
        all_results = [r for y in yearly_results.values() for r in y]
        all_total = sum(all_results) if all_results else 0
        message += f"{EMOJIS['sum']} *Gesamtergebnis*: {format_percent(all_total)}"
    else:
        message += f"Keine Daten verfügbar.\n\n{EMOJIS['refresh']} Versuche /refresh, falls Daten fehlen."
    await update.message.reply_text(message, reply_markup=KEYBOARD, parse_mode="Markdown")

async def handle_keyboard_buttons(update, context):
    text = update.message.text
    if text == "ℹ️ Info":
        await info(update, context)
    elif text == f"{EMOJIS['result']} Letztes Ergebnis":
        await result(update, context)
    elif text == f"{EMOJIS['month']} Ergebnisse (Aktuelle Woche)":
        await daily(update, context)
    elif text == f"{EMOJIS['month']} Wochen (Aktueller Monat)":
        await weekly(update, context)
    elif text == f"{EMOJIS['month']} Ergebnisse (Monate)":
        await monthly(update, context)
    elif text == f"{EMOJIS['year']} Ergebnisse (Jahre)":
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
    app.add_handler(CommandHandler("monthly", monthly))
    app.add_handler(CommandHandler("yearly", yearly))
    app.add_handler(CommandHandler("refresh", refresh))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_keyboard_buttons))
    app.run_webhook(
        listen="0.0.0.0",
        port=int(os.getenv("PORT", 8443)),
        url_path=TOKEN,
        webhook_url=f"https://{os.getenv('RENDER_EXTERNAL_HOSTNAME')}/{TOKEN}"
    )

if __name__ == "__main__":
    main()