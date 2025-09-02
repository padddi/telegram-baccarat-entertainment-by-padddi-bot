# airtable.py
import os
import requests
import logging
from datetime import datetime
from config import DATE_FORMAT

# Konfiguriere Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def fetch_airtable_data(context, year):
    """Holt Daten aus Airtable für ein gegebenes Jahr und speichert sie im Cache."""
    cache_key = f"airtable_cache_{year}"
    timestamp_key = f"cache_timestamp_{year}"
    if cache_key in context.bot_data and timestamp_key in context.bot_data:
        if (datetime.now() - context.bot_data[timestamp_key]).seconds < 300:
            logger.debug(f"Returning cached data for year {year}")
            return context.bot_data[cache_key]
    
    headers = {"Authorization": f"Bearer {os.getenv('AIRTABLE_TOKEN')}"}
    base_id = os.getenv(f"AIRTABLE_BASE_{year}")
    table_id = os.getenv(f"AIRTABLE_TBL_{year}")
    if not base_id or not table_id:
        logger.error(f"Missing Airtable configuration for year {year}: BASE={base_id}, TBL={table_id}")
        return []
    records = []
    params = {"sort[0][field]": "Date", "sort[0][direction]": "desc"}
    url = f"https://api.airtable.com/v0/{base_id}/{table_id}"
    
    try:
        while True:
            logger.debug(f"Sending GET request to {url} with params {params}")
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
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
        error_message = f"Error fetching Airtable data for {year}: {e}"
        if hasattr(e, 'response') and e.response is not None:
            error_message += f" - Status: {e.response.status_code}, Response: {e.response.text}, URL: {url}"
            if e.response.status_code == 429:
                logger.warning("Rate limit exceeded, consider implementing retry logic")
        logger.error(error_message)
        return context.bot_data.get(cache_key, [])
    
    context.bot_data[cache_key] = records
    context.bot_data[timestamp_key] = datetime.now()
    logger.info(f"Successfully fetched {len(records)} records for year {year}")
    return records

async def get_all_data(context):
    """Kombiniert Daten aus allen Jahren."""
    data = []
    for year in ["2023", "2024", "2025"]:
        data.extend(await fetch_airtable_data(context, year))
    logger.info(f"Combined {len(data)} records from all years")
    return data

async def get_current_year_data(context):
    """Holt Daten nur für das aktuelle Jahr (2025)."""
    data = await fetch_airtable_data(context, "2025")
    logger.info(f"Fetched {len(data)} records for current year 2025")
    return data

async def add_chat_id_to_notifications(context, chat_id):
    """Fügt eine Chat-ID zur Benachrichtigungs-Tabelle hinzu oder aktualisiert sie."""
    headers = {"Authorization": f"Bearer {os.getenv('AIRTABLE_TOKEN')}", "Content-Type": "application/json"}
    base_id = os.getenv("AIRTABLE_NOTIFICATION_BASE")
    table_id = os.getenv("AIRTABLE_NOTIFICATION_TBL")
    if not base_id or not table_id:
        logger.error(f"Missing Airtable configuration: BASE={base_id}, TBL={table_id}")
        return False, "Fehler beim Anmelden der Benachrichtigung"

    # Daten für den neuen Eintrag
    record_data = {
        "records": [
            {
                "fields": {
                    "ChatId": int(chat_id),  # Geändert: Integer statt String
                    "Subscribed": datetime.now().strftime("%Y-%m-%d")
                }
            }
        ]
    }

    # Daten für den aktualisierten Eintrag (PATCH)
    update_data = {
        "fields": {
            "ChatId": int(chat_id),  # Geändert: Integer statt String
            "Subscribed": datetime.now().strftime("%Y-%m-%d")
        }
    }

    url = f"https://api.airtable.com/v0/{base_id}/{table_id}"
    params = {"filterByFormula": f"{{ChatId}} = {chat_id}"}  # Geändert: Keine Anführungszeichen für Integer
    try:
        # Suche nach vorhandenem Eintrag
        logger.debug(f"Sending GET request to {url} with params {params}")
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        existing_records = data.get("records", [])

        if existing_records:
            # Aktualisiere bestehenden Eintrag
            record_id = existing_records[0]["id"]
            logger.debug(f"Sending PATCH request to {url}/{record_id} with data {update_data}")
            response = requests.patch(f"{url}/{record_id}", headers=headers, json=update_data)
            response.raise_for_status()
            logger.info(f"Chat-ID {chat_id} erfolgreich aktualisiert in Airtable.")
        else:
            # Füge neuen Eintrag hinzu
            logger.debug(f"Sending POST request to {url} with data {record_data}")
            response = requests.post(url, headers=headers, json=record_data)
            response.raise_for_status()
            logger.info(f"Chat-ID {chat_id} erfolgreich hinzugefügt in Airtable.")
        return True, None
    except requests.RequestException as e:
        error_message = f"Error adding chat_id {chat_id} to Airtable: {e}"
        if hasattr(e, 'response') and e.response is not None:
            error_message += f" - Status: {e.response.status_code}, Response: {e.response.text}, URL: {url}"
            if e.response.status_code == 429:
                logger.warning("Rate limit exceeded, consider implementing retry logic")
            elif e.response.status_code == 422:
                logger.error(f"Invalid request, check field names or required fields: {record_data if not existing_records else update_data}")
            elif e.response.status_code == 401:
                logger.error("Authentication error, verify AIRTABLE_TOKEN")
            elif e.response.status_code == 403:
                logger.error("Permission error, check access rights for the Airtable base")
            elif e.response.status_code == 404:
                logger.error(f"Base or table not found, verify AIRTABLE_NOTIFICATION_BASE={base_id}, AIRTABLE_NOTIFICATION_TBL={table_id}")
        logger.error(error_message)
        return False, "Fehler beim Anmelden der Benachrichtigung"

async def remove_chat_id_from_notifications(context, chat_id):
    """Entfernt eine Chat-ID aus der Benachrichtigungs-Tabelle."""
    headers = {"Authorization": f"Bearer {os.getenv('AIRTABLE_TOKEN')}"}
    base_id = os.getenv("AIRTABLE_NOTIFICATION_BASE")
    table_id = os.getenv("AIRTABLE_NOTIFICATION_TBL")
    if not base_id or not table_id:
        logger.error(f"Missing Airtable configuration: BASE={base_id}, TBL={table_id}")
        return False, "Fehler beim Abmelden der Benachrichtigung"

    url = f"https://api.airtable.com/v0/{base_id}/{table_id}"
    params = {"filterByFormula": f"{{ChatId}} = {chat_id}"}  # Geändert: Keine Anführungszeichen für Integer
    try:
        logger.debug(f"Sending GET request to {url} with params {params}")
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        records = data.get("records", [])

        if records:
            # Lösche den Eintrag
            record_id = records[0]["id"]
            logger.debug(f"Sending DELETE request to {url}/{record_id}")
            response = requests.delete(f"{url}/{record_id}", headers=headers)
            response.raise_for_status()
            logger.info(f"Chat-ID {chat_id} erfolgreich aus Airtable entfernt.")
        else:
            logger.info(f"Chat-ID {chat_id} nicht in Airtable gefunden (ignoriert).")
        return True, None
    except requests.RequestException as e:
        error_message = f"Error removing chat_id {chat_id} from Airtable: {e}"
        if hasattr(e, 'response') and e.response is not None:
            error_message += f" - Status: {e.response.status_code}, Response: {e.response.text}, URL: {url}"
            if e.response.status_code == 429:
                logger.warning("Rate limit exceeded, consider implementing retry logic")
            elif e.response.status_code == 401:
                logger.error("Authentication error, verify AIRTABLE_TOKEN")
            elif e.response.status_code == 403:
                logger.error("Permission error, check access rights for the Airtable base")
            elif e.response.status_code == 404:
                logger.error(f"Base or table not found, verify AIRTABLE_NOTIFICATION_BASE={base_id}, AIRTABLE_NOTIFICATION_TBL={table_id}")
        logger.error(error_message)
        return False, "Fehler beim Abmelden der Benachrichtigung"