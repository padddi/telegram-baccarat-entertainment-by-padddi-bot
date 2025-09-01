import sys
import os
import requests
from telegram import Bot
from telegram.constants import ParseMode
import asyncio

# Konfiguration (aus Umgebungsvariablen laden – in GitHub Secrets speichern)
AIRTABLE_TOKEN = os.getenv('AIRTABLE_TOKEN')  # Dein Airtable Token
AIRTABLE_NOTIFICATION_BASE = os.getenv('AIRTABLE_NOTIFICATION_BASE')  # Ersetze mit deiner Base ID
AIRTABLE_NOTIFICATION_TBL = os.getenv('AIRTABLE_NOTIFICATION_TBL')  # Ersetze mit Table ID oder Name
CHAT_ID_FIELD = 'ChatId'  # Festgelegter Feldname für Chat-IDs
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')  # Dein Telegram Bot Token

# Markdown-Nachricht (vom User bereitgestellt – hier als Beispiel; kann als Argument übergeben werden)
# Für MarkdownV2 müssen bestimmte Zeichen escaped werden (z.B. '.', '!', '-')
MESSAGE = """
🚨 **Neue Benachrichtigung!**

- **Titel**: Beispiel-Titel
- **Details**: Hier kommt dein Markdown-Inhalt hin.
- **Link**: [Klicke hier](https://example.com)

Mehr Infos folgen.
"""  # Du kannst das dynamisch machen, z.B. via sys.argv[1]

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

async def send_telegram_message(bot, chat_id, message):
    """
    Sendet eine Markdown-Nachricht an eine Chat-ID via python-telegram-bot SDK.
    """
    try:
        await bot.send_message(
            chat_id=chat_id,
            text=message,
            parse_mode=ParseMode.MARKDOWN_V2  # MarkdownV2 für Telegram
        )
        print(f"Nachricht gesendet an {chat_id}")
    except Exception as e:
        print(f"Fehler beim Senden an {chat_id}: {e}")

async def main():
    # Optional: Nachricht als Kommandozeilen-Argument übernehmen (z.B. für dynamische Inhalte)
    if len(sys.argv) > 1:
        global MESSAGE
        MESSAGE = sys.argv[1]
    
    # Chat-IDs holen
    chat_ids = get_chat_ids()
    print(f"Gefundene Chat-IDs: {len(chat_ids)}")
    
    # Telegram Bot initialisieren
    bot = Bot(token=TELEGRAM_TOKEN)
    
    # Für jede Chat-ID senden
    for chat_id in chat_ids:
        await send_telegram_message(bot, chat_id, MESSAGE)
    
    print("Alle Nachrichten versendet.")

if __name__ == "__main__":
    if not AIRTABLE_TOKEN or not TELEGRAM_TOKEN or not AIRTABLE_NOTIFICATION_BASE or not AIRTABLE_NOTIFICATION_TBL:
        raise ValueError("Eine oder mehrere Umgebungsvariablen fehlen: AIRTABLE_TOKEN, TELEGRAM_TOKEN, AIRTABLE_NOTIFICATION_BASE, AIRTABLE_NOTIFICATION_TBL")
    
    # Asynchronen Main ausführen
    asyncio.run(main())