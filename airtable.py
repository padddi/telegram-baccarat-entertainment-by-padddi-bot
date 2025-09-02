# airtable.py
import os
import requests
from datetime import datetime
from config import DATE_FORMAT

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

async def add_chat_id_to_notifications(context, chat_id):
    """Fügt eine Chat-ID zur Benachrichtigungs-Tabelle hinzu oder aktualisiert sie."""
    headers = {"Authorization": f"Bearer {os.getenv('AIRTABLE_TOKEN')}", "Content-Type": "application/json"}
    base_id = os.getenv("AIRTABLE_NOTIFICATION_BASE")
    table_id = os.getenv("AIRTABLE_NOTIFICATION_TBL")
    if not base_id or not table_id:
        return False, "Fehler: Airtable-Konfiguration fehlt."

    # Prüfe, ob die Chat-ID bereits existiert
    url = f"https://api.airtable.com/v0/{base_id}/{table_id}"
    params = {"filterByFormula": f"{{ChatId}} = '{chat_id}'"}
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        existing_records = data.get("records", [])

        # Daten für den neuen oder aktualisierten Eintrag
        record_data = {
            "fields": {
                "ChatId": str(chat_id),
                "Subscribed": datetime.now().strftime("%Y-%m-%d")
            }
        }

        if existing_records:
            # Aktualisiere bestehenden Eintrag
            record_id = existing_records[0]["id"]
            response = requests.patch(f"{url}/{record_id}", headers=headers, json=record_data)
            response.raise_for_status()
        else:
            # Füge neuen Eintrag hinzu
            response = requests.post(url, headers=headers, json={"records": [record_data]})
            response.raise_for_status()
        return True, None
    except requests.RequestException as e:
        print(f"Error adding chat_id to Airtable: {e}")
        return False, f"Fehler beim Hinzufügen der Chat-ID. Bitte versuche es später erneut: {str(e)}"

async def remove_chat_id_from_notifications(context, chat_id):
    """Entfernt eine Chat-ID aus der Benachrichtigungs-Tabelle."""
    headers = {"Authorization": f"Bearer {os.getenv('AIRTABLE_TOKEN')}"}
    base_id = os.getenv("AIRTABLE_NOTIFICATION_BASE")
    table_id = os.getenv("AIRTABLE_NOTIFICATION_TBL")
    if not base_id or not table_id:
        return False, "Fehler: Airtable-Konfiguration fehlt."

    # Suche nach der Chat-ID
    url = f"https://api.airtable.com/v0/{base_id}/{table_id}"
    params = {"filterByFormula": f"{{ChatId}} = '{chat_id}'"}
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        records = data.get("records", [])

        if records:
            # Lösche den Eintrag
            record_id = records[0]["id"]
            response = requests.delete(f"{url}/{record_id}", headers=headers)
            response.raise_for_status()
        return True, None
    except requests.RequestException as e:
        print(f"Error removing chat_id from Airtable: {e}")
        return False, f"Fehler beim Entfernen der Chat-ID. Bitte versuche es später erneut: {str(e)}"