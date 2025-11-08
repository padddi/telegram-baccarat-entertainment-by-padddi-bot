import sys
import os
import requests
from telegram import Bot
from telegram.constants import ParseMode
import asyncio
import re
from datetime import datetime

# Relativen Pfad zu airtable.py hinzufügen
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from airtable import get_current_year_data  # Import der Funktion aus airtable.py im Root-Verzeichnis

# Konfiguration (aus Umgebungsvariablen laden – in GitHub Secrets speichern)
AIRTABLE_TOKEN = os.getenv('AIRTABLE_TOKEN')  # Dein Airtable Token
AIRTABLE_NOTIFICATION_BASE = os.getenv('AIRTABLE_NOTIFICATION_BASE')  # Ersetze mit deiner Base ID
AIRTABLE_NOTIFICATION_TBL = os.getenv('AIRTABLE_NOTIFICATION_TBL')  # Ersetze mit Table ID oder Name
CHAT_ID_FIELD = 'ChatId'  # Festgelegter Feldname für Chat-IDs
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')  # Dein Telegram Bot Token

# Konstanten für die Nachricht
EMOJI_ALERT = "🚨"
EMOJI_RESULT = "📊"
DASHBOARD_LINK = "https://app.baccarat-entertainment.com"

def escape_markdown_v2(text):
    """
    Escaped reservierte Zeichen für Telegram MarkdownV2.
    """
    reserved_chars = r'([_\*\[\]\(\)~`>#\+-=|{}.!])'
    return re.sub(reserved_chars, r'\\\1', text)

def get_chat_ids():
    """
    Holt alle Chat-IDs aus Airtable via API.
    """
    url = f"https://api.airtable.com/v0/{AIRTABLE_NOTIFICATION_BASE}/{AIRTABLE_NOTIFICATION_TBL}?fields%5B%5D={CHAT_ID_FIELD}"
    headers = {
        'Authorization': f'Bearer {AIRTABLE_TOKEN}',
        'Content-Type': 'application/json'
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Fehler werfen, wenn API-Call scheitert
    
    records = response.json().get('records', [])
    chat_ids = [record['fields'].get(CHAT_ID_FIELD) for record in records if CHAT_ID_FIELD in record['fields']]
    
    if not chat_ids:
        raise ValueError("Keine Chat-IDs in Airtable gefunden.")
    
    return chat_ids

async def get_latest_result(context):
    """
    Holt das neueste Ergebnis aus Airtable für das aktuelle Jahr (2025).
    """
    data = await get_current_year_data(context)
    if not data:
        raise ValueError("Keine Daten für das aktuelle Jahr gefunden.")
    
    # Sortiere nach Datum absteigend, um das neueste Ergebnis zu erhalten
    latest_record = max(data, key=lambda x: datetime.strptime(x['Date'], "%Y-%m-%d"))
    return latest_record['Date'], latest_record['Result']

async def send_telegram_message(bot, chat_id, message):
    """
    Sendet eine Markdown-Nachricht an eine Chat-ID via python-telegram-bot SDK.
    """
    try:
        escaped_message = escape_markdown_v2(message)
        await bot.send_message(
            chat_id=chat_id,
            text=escaped_message,
            parse_mode=ParseMode.MARKDOWN_V2
        )
        print(f"Nachricht gesendet an {chat_id}")
    except Exception as e:
        print(f"Fehler beim Senden an {chat_id}: {e}")

async def main():
    # Telegram Bot initialisieren
    bot = Bot(token=TELEGRAM_TOKEN)
    
    # Kontext für airtable.py (bot_data für Caching)
    context = type('Context', (), {'bot_data': {}})()
    
    # Neuestes Ergebnis holen
    try:
        date, result = await get_latest_result(context)
    except ValueError as e:
        print(f"Fehler beim Abrufen der Daten: {e}")
        return

    # Ergebnis als Prozentsatz formatieren (angenommen, es ist eine Zahl)
    try:
        result_value = float(result)  # Konvertiere Result zu Float für die Prüfung
        result_formatted = f"{result_value:.2f}%"  # Formatierte Darstellung
    except ValueError:
        result_value = result  # Falls kein Float, Originalwert behalten
        result_formatted = f"{result}%"  # Falls bereits ein String, nur % anhängen
    
    # Prüfe, ob Result gleich 0 ist
    isNullRound = result_value == 0
    
    # Nachricht basierend auf isNullRound erstellen
    if isNullRound:
        MESSAGE = f"{EMOJI_ALERT}{EMOJI_ALERT}{EMOJI_ALERT} Nullrunde {EMOJI_ALERT}{EMOJI_ALERT}{EMOJI_ALERT}\n\n" \
                  f"Leider gab es diesmal kein Ergebnis. \n\n" \
                  f"Details im Dashboard: {DASHBOARD_LINK}\n\n" \
                  f"{date}: {EMOJI_RESULT} {result_formatted}"
    else:
        MESSAGE = f"{EMOJI_ALERT}{EMOJI_ALERT}{EMOJI_ALERT} Neues Ergebnis {EMOJI_ALERT}{EMOJI_ALERT}{EMOJI_ALERT}\n\n" \
                  f"Das aktuelle Ergebnis steht jetzt im Dashboard von Baccarat Entertainment zur Verfügung. \n\n" \
                  f"{DASHBOARD_LINK}\n\n" \
                  f"{date}: {EMOJI_RESULT} {result_formatted}"
    
    # Optional: Nachricht als Kommandozeilen-Argument übernehmen (überschreibt die generierte Nachricht)
    if len(sys.argv) > 1:
        MESSAGE = sys.argv[1]
    
    # Chat-IDs holen
    chat_ids = get_chat_ids()
    print(f"Gefundene Chat-IDs: {len(chat_ids)}")
    
    # Für jede Chat-ID senden
    for chat_id in chat_ids:
        await send_telegram_message(bot, chat_id, MESSAGE)
    
    print("Alle Nachrichten versendet.")

if __name__ == "__main__":
    if not AIRTABLE_TOKEN or not TELEGRAM_TOKEN or not AIRTABLE_NOTIFICATION_BASE or not AIRTABLE_NOTIFICATION_TBL:
        raise ValueError("Eine oder mehrere Umgebungsvariablen fehlen: AIRTABLE_TOKEN, TELEGRAM_TOKEN, AIRTABLE_NOTIFICATION_BASE, AIRTABLE_NOTIFICATION_TBL")
    
    # Asynchronen Main ausführen
    asyncio.run(main())