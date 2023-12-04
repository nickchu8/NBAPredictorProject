from game_data_ingest_scraping import scrape_games_to_csv
import pandas as pd
import sqlite3
from datetime import date
import collections
import os
from utils import table_exists, date_range, sqlite_date_string


def games_df_for_dates(dates: list[date]):
    data_location = "scraped_games.csv"
    scrape_games_to_csv(data_location, dates)
    if os.path.getsize(data_location) > 0:
        df = pd.read_csv(data_location)
        df["date"] = pd.to_datetime(df["date"])
        return df
    else:
        return None


def put_dates_in_db(dates: collections.abc.Iterable[date]):
    def date_is_in_db(conn, date):
        c = conn.cursor()
        q = f"SELECT EXISTS(SELECT 1 FROM games WHERE date = ?);"
        c.execute(q, (sqlite_date_string(date),))
        exists = c.fetchone()[0]
        return exists == 1

    with sqlite3.connect("games.db") as conn:
        dates_to_scrape = None
        if table_exists(conn, "games"):
            dates_to_scrape = list(filter(lambda d: not date_is_in_db(conn, d), dates))
        else:
            dates_to_scrape = list(dates)

        if len(dates_to_scrape) == 0:
            print("All dates have already been scraped")
            return
        print(f"{len(dates_to_scrape)} dates have to be scraped")
        df = games_df_for_dates(dates_to_scrape)
        if df is not None:
            df.to_sql("games", conn, if_exists="append", index=False)


def main():
    some_dates = date_range(date(2000, 1, 1), date(2000, 1, 4))
    put_dates_in_db(some_dates)

    with sqlite3.connect("games.db") as conn:
        c = conn.cursor()
        q = f"SELECT COUNT(*) FROM games;"
        c.execute(q)
        print(c.fetchone())

    with sqlite3.connect("games.db") as conn:
        c = conn.cursor()
        q = f"SELECT * FROM games WHERE date = ?;"
        c.execute(q, (str(date(2000, 1, 1)),))
        print(c.fetchone())


if __name__ == "__main__":
    main()
    exit()
    with sqlite3.connect("games.db") as conn:
        c = conn.cursor()
        q = f"SELECT date FROM games LIMIT 5;"
        # c.execute(q, (sqlite_date_string(date(2000, 1, 1)),))
        ds = sqlite_date_string(date(2000, 1, 2))
        print(ds)
        c.execute(q)
        print(c.fetchall())
