# config.py
from telegram import ReplyKeyboardMarkup

DATE_FORMAT = "%d.%m.%Y"  # Beispiel: 02.09.2025
PERCENT_FORMAT = ".2f"    # Für 12,34%

EMOJIS = {
    "result": "✅",
    "week": "📈",
    "sum": "📊",
    "month": "🗓️",
    "year": "🗂️",
    "refresh": "🔄"
}

WEEKDAYS = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag"]

KEYBOARD = ReplyKeyboardMarkup([
    ["ℹ️ Info", f"{EMOJIS['result']} Letztes Ergebnis"],
    [f"{EMOJIS['month']} Ergebnisse (Aktuelle Woche)", f"{EMOJIS['month']} Wochen (Aktueller Monat)"],
    [f"{EMOJIS['month']} Ergebnisse (Monate)", f"{EMOJIS['year']} Ergebnisse (Jahre)"]
], resize_keyboard=True)

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