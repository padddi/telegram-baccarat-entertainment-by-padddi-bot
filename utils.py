# utils.py
from datetime import datetime, timedelta
from config import DATE_FORMAT, PERCENT_FORMAT

def format_percent(value):
    """Formatiert einen Float- oder Integer-Wert als ###,##%."""
    return f"{float(value):{PERCENT_FORMAT}}%".replace(".", ",")

def get_week_date_range(week, year):
    """Gibt den Datumsbereich einer Woche (Montag bis Freitag) zurück."""
    first_day = datetime.strptime(f"{year}-W{week-1}-1", "%Y-W%W-%w")
    last_day = first_day + timedelta(days=4)  # Freitag
    return first_day.strftime(DATE_FORMAT), last_day.strftime(DATE_FORMAT)
    