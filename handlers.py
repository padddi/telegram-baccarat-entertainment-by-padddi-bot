# handlers.py
from datetime import datetime, timedelta
from telegram import Update
from telegram.ext import ContextTypes
from config import DASHBOARD_MESSAGE, KEYBOARD, EMOJIS, WEEKDAYS, DATE_FORMAT
from utils import format_percent, get_week_date_range
from airtable import get_current_year_data, get_all_data, add_chat_id_to_notifications, remove_chat_id_from_notifications

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(DASHBOARD_MESSAGE, reply_markup=KEYBOARD, parse_mode="Markdown")

async def dashboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(DASHBOARD_MESSAGE, reply_markup=KEYBOARD, parse_mode="Markdown")

async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(DASHBOARD_MESSAGE, reply_markup=KEYBOARD, parse_mode="Markdown")

async def refresh(update: Update, context: ContextTypes.DEFAULT_TYPE):
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

async def result(update: Update, context: ContextTypes.DEFAULT_TYPE):
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

async def daily(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
        total = sum(r["Result"] for r in week_data) if week_data else 0
        message += f"\n{EMOJIS['sum']} *Wochenergebnis*: {format_percent(total)}"
    else:
        message += f"Keine Ergebnisse für die aktuelle Woche.\n\n{EMOJIS['refresh']} Versuche /refresh, falls Daten fehlen."
    await update.message.reply_text(message, reply_markup=KEYBOARD, parse_mode="Markdown")

async def weekly(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
            month_results = [r for w in weekly_results.values() for r in w]
            month_total = sum(month_results) if month_results else 0
            message += f"{EMOJIS['sum']} *Monatsergebnis*: {format_percent(month_total)}\n\n\n"
        else:
            message += f"Keine Ergebnisse für den aktuellen Monat.\n\n{EMOJIS['refresh']} Versuche /refresh, falls Daten fehlen."
    else:
        message += f"Keine Daten verfügbar.\n\n{EMOJIS['refresh']} Versuche /refresh, falls Daten fehlen."
    await update.message.reply_text(message, reply_markup=KEYBOARD, parse_mode="Markdown")

async def monthly(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
        year_results = [r for m in monthly_results.values() for r in m]
        year_total = sum(year_results) if year_results else 0
        message += f"{EMOJIS['sum']} *Jahresergebnis*: {format_percent(year_total)}"
    else:
        message += f"Keine Daten verfügbar.\n\n{EMOJIS['refresh']} Versuche /refresh, falls Daten fehlen."
    await update.message.reply_text(message, reply_markup=KEYBOARD, parse_mode="Markdown")

async def yearly(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
        all_results = [r for y in yearly_results.values() for r in y]
        all_total = sum(all_results) if all_results else 0
        message += f"{EMOJIS['sum']} *Gesamtergebnis*: {format_percent(all_total)}"
    else:
        message += f"Keine Daten verfügbar.\n\n{EMOJIS['refresh']} Versuche /refresh, falls Daten fehlen."
    await update.message.reply_text(message, reply_markup=KEYBOARD, parse_mode="Markdown")

async def chatid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Gibt die Chat-ID des aktuellen Chats zurück."""
    chat_id = update.message.chat.id
    message = f"Deine Chat-ID ist: {chat_id}"
    await update.message.reply_text(message, reply_markup=KEYBOARD, parse_mode="Markdown")

async def subscribe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Trägt die Chat-ID in die Benachrichtigungs-Tabelle ein."""
    if update.message.chat.type != "private":
        await update.message.reply_text(
            "Dieser Befehl ist nur für private Chats verfügbar.",
            reply_markup=KEYBOARD,
            parse_mode="Markdown"
        )
        return
    chat_id = update.message.chat.id
    success, error = await add_chat_id_to_notifications(context, chat_id)
    if success:
        message = "✅ Du hast dich erfolgreich für Benachrichtigungen angemeldet!"
    else:
        message = "❌ Fehler beim Anmelden der Benachrichtigung"
    await update.message.reply_text(message, reply_markup=KEYBOARD, parse_mode="Markdown")

async def unsubscribe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Entfernt die Chat-ID aus der Benachrichtigungs-Tabelle."""
    if update.message.chat.type != "private":
        await update.message.reply_text(
            "Dieser Befehl ist nur für private Chats verfügbar.",
            reply_markup=KEYBOARD,
            parse_mode="Markdown"
        )
        return
    chat_id = update.message.chat.id
    success, error = await remove_chat_id_from_notifications(context, chat_id)
    if success:
        message = "✅ Du bist nicht mehr für Benachrichtigungen angemeldet."
    else:
        message = "❌ Fehler beim Abmelden der Benachrichtigung"
    await update.message.reply_text(message, reply_markup=KEYBOARD, parse_mode="Markdown")

async def handle_keyboard_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
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