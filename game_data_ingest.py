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


def get_average_stats_over_period(
    conn, team_slug: str, start_date: date, end_date: date
):
    """
    Return a DataFrame with one row containing a team's average statistics from
    `start_date` to `end_date`, not including `end_date`.
    If the team has no games in that date range, return None.
    """
    relevant_stats = [
        "fieldGoalsMade",
        "fieldGoalsAttempted",
        "threePointersMade",
        "threePointersAttempted",
        "freeThrowsMade",
        "freeThrowsAttempted",
        "reboundsOffensive",
        "reboundsDefensive",
        "assists",
        "steals",
        "blocks",
        "foulsPersonal",
        "points",
    ]
    start_date_string = sqlite_date_string(start_date)
    end_date_string = sqlite_date_string(end_date)
    def query_stat_as_home(stat_name):
        return f"SELECT {'hometeam_' + stat_name} AS {stat_name} FROM games \
                 WHERE hometeam_slug = '{team_slug}' \
                    AND '{start_date_string}' <= date \
                    AND date < '{end_date_string}'"

    def query_stat_as_away(stat_name):
        return f"SELECT {'awayteam_' + stat_name} AS {stat_name} FROM games \
                 WHERE awayteam_slug = '{team_slug}' \
                    AND '{start_date_string}' <= date \
                    AND date < '{end_date_string}'"

    def get_value_of_stat(stat_name):
        subq1 = query_stat_as_home(stat_name)
        subq2 = query_stat_as_away(stat_name)
        c = conn.cursor()
        c.execute(f"SELECT AVG({stat_name}) FROM ({subq1} UNION ALL {subq2});")
        return c.fetchone()[0]

    def get_number_of_games_played():
        subq1 = query_stat_as_home(relevant_stats[0])
        subq2 = query_stat_as_away(relevant_stats[0])
        c = conn.cursor()
        c.execute(f"SELECT COUNT(*) FROM ({subq1} UNION ALL {subq2});")
        return c.fetchone()[0]

    game_count = get_number_of_games_played()
    if game_count == 0:
        return None
    row = [get_value_of_stat(s) for s in relevant_stats]
    row.append(game_count)
    df = pd.DataFrame(data=[row], columns=relevant_stats + ["gamesCount"])
    return df

def generate_training_data_for_season(season_begin: date, season_end: date):
    # TODO
    # for each game in the season:
    # call get_average_stats_over_period(home team, season_begin, game_date)
    # call get_average_stats_over_period(away team, season_begin, game_date)
    # if either is None: this is one of the first games, don't use it
    # otherwise, make a dataframe row with the home stats, away stats, and game_winner

    # At the end, return the dataframe created
    pass


def main():
    some_dates = date_range(date(2000, 1, 1), date(2000, 1, 4))
    put_dates_in_db(some_dates)

    with sqlite3.connect("games.db") as conn:
        c = conn.cursor()
        q = f"SELECT COUNT(*) FROM games;"
        c.execute(q)
        print("Total count of games in the database:", c.fetchone()[0])

    with sqlite3.connect("games.db") as conn:
        nuggets_stats = get_average_stats_over_period(
            conn, "nuggets", date(2000, 1, 1), date(2001, 1, 1)
        )
        print("---- Nuggets stats ----")
        print(nuggets_stats)


if __name__ == "__main__":
    main()
