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