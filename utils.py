import sqlite3
from datetime import datetime, date, timedelta


def table_exists(conn: sqlite3.Connection, table_name: str) -> bool:
    c = conn.cursor()
    q = f"SELECT 1 FROM sqlite_master WHERE type='table' AND name=?;"
    c.execute(q, (table_name,))
    return len(c.fetchall()) > 0


def date_range(first: date, last: date):
    """
    A generator over dates from `first` to `last` inclusive.
    """
    assert first <= last
    ndays = int((last - first).days)
    return (first + timedelta(n) for n in range(ndays + 1))


def sqlite_date_string(d: date) -> str:
    return str(datetime(d.year, d.month, d.day))

def date_from_sqlite_string(s: str) -> date:
    return datetime.fromisoformat(s).date()
