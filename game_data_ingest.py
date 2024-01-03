from game_data_ingest_scraping import scrape_games_to_csv
import pandas as pd
import sqlite3
from datetime import date
import collections
import os
from utils import table_exists, date_range, sqlite_date_string, date_from_sqlite_string


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


def generate_training_data_for_season(conn, season_begin: date, season_end: date):
    """
    Return a DataFrame with one row for each non-starting game between
    `season_begin` and `season_end`, inclusive. A non-starting game is one
    where both teams in the game have played one or more games within
    `season_begin`, `season_end` prior to that game.
    The columns in the DataFrame are:
      - average statistics for the home team's previous performance, with
    the prefix "hometeam_"
      - the same statistics for the away team, with the prefix "awayteam_"
      - the column "winner_is_home_team" with a value of 1 or 0

    Precondition: all the NBA games between `season_begin` and `season_end` inclusive
    are loaded into the SQLite database corresponding to `conn`.
    Call `put_dates_in_db(date_range(season_begin, season_end))` to meet this
    precondition.
    """
    begin_str = sqlite_date_string(season_begin)
    end_str = sqlite_date_string(season_end)
    q = f"SELECT hometeam_slug, awayteam_slug, winner_is_home_team, date \
          FROM games \
          WHERE '{begin_str}' <= date AND date <= '{end_str}'"
    c = conn.cursor()
    c.execute(q)

    # We want to use the statistics columns returned by `get_average_stats_over_period`.
    # Rather than set the columns right here, we initialize `result` to None and will set it
    # to non-None once we obtain the first row that belongs in it.
    result = None
    for home_slug, away_slug, winner_is_home_team, game_date in c.fetchall():
        game_date = date_from_sqlite_string(game_date)
        home_history = get_average_stats_over_period(
            conn, home_slug, season_begin, game_date
        )
        away_history = get_average_stats_over_period(
            conn, away_slug, season_begin, game_date
        )
        if home_history is None or away_history is None:
            # This is a starting game so we don't include it
            continue
        home_history.drop(["gamesCount"], axis=1, inplace=True)
        away_history.drop(["gamesCount"], axis=1, inplace=True)
        home_history.rename(lambda stat: "hometeam_" + stat, axis=1, inplace=True)
        away_history.rename(lambda stat: "awayteam_" + stat, axis=1, inplace=True)
        winner_column = pd.Series([winner_is_home_team], name="winner_is_home_team")

        game_datum = pd.concat(
            [home_history, away_history, winner_column],
            axis="columns",
        )

        if result is None:
            result = game_datum
        else:
            result = pd.concat([result, game_datum], ignore_index=True)
    return result


def main():
    some_dates = date_range(date(2000, 10, 31), date(2023, 4, 9))
    put_dates_in_db(some_dates)

    with sqlite3.connect("games.db") as conn:
        c = conn.cursor()
        q = f"SELECT COUNT(*) FROM games;"
        c.execute(q)
        print("Total count of games in the database:", c.fetchone()[0])

    with sqlite3.connect("games.db") as conn:
        df = generate_training_data_for_season(
            conn, date(2000, 10, 31), date(2023, 4, 9)
        )
        print("---- Training Data ----")
        print(df)


if __name__ == "__main__":
    main()
