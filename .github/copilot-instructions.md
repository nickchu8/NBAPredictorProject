# NBAPredictorProject – AI Agent Guide

Purpose: Help AI agents be productive fast in this repo by capturing the actual architecture, workflows, conventions, and gotchas observed in code.

## Big picture
- Goal: Predict NBA playoff outcomes by training a Keras model on regular-season game data, then simulating matchups.
- Data flow:
  1) Scrape NBA.com game pages per date into CSV (Scrapy)
  2) Append CSV rows into SQLite `games.db` (table `games`)
  3) Build training rows by averaging each team’s prior regular-season stats up to the game date (26 features = 13 stats x 2 teams)
  4) Train/evaluate models in notebooks; use averages to predict hypothetical matchups

## Key components and boundaries
- Scraping (external I/O)
  - `nba_games_scraper/nba_games_scraper/spiders/games_spider.py`
    - Emits one row per game: `date`, `hometeam_slug`, `awayteam_slug`, `winner_is_home_team` plus 13 stats per team prefixed with `hometeam_` / `awayteam_`.
    - Selects JSON from `<script id="__NEXT_DATA__">` and asserts complete stats are present. Team IDs are NBA.com `teamSlug` (lowercase).
  - `game_data_ingest_scraping.py`
    - Wrapper for Scrapy that runs in a separate process (Twisted isn’t re-runnable). Use `scrape_games_to_csv(output_file_path, dates)`.
- Ingest + Features (SQLite + Pandas)
  - `game_data_ingest.py`
    - `put_dates_in_db(dates)`: Avoids duplicate dates; calls the scraper; appends CSV into `games.db`.
    - `get_average_stats_over_period(conn, team_slug, start_date, end_date)`: Returns one-row DataFrame with the 13 stats’ averages and `gamesCount`.
    - `generate_training_data_for_season(conn, season_begin, season_end)`: For each non-starting game, concatenates home/away averages (prefixes) and adds label `winner_is_home_team`.
  - `utils.py`: `date_range`, `sqlite_date_string`, `date_from_sqlite_string`, `table_exists`.
- Modeling + UI
  - `gui.py`: PySimpleGUI builder; returns `(model, season_string)`. Hidden layers are user-defined; input layer shape is 26; output is a single sigmoid.
  - `main.ipynb`: Orchestrates scraping/ingest, defines season date ranges, trains/evaluates, and predicts playoff matchups. See helper `get_matchup_df` pattern (drop `gamesCount`, add prefixes, concat).

## Conventions and invariants
- Stats list is the contract: keep the same 13-stat set in both places
  - Spider: `relevant_stats` set
  - Ingest: `relevant_stats` list in `get_average_stats_over_period`
  - Order matters for model input; total features = 26.
- Column names: `hometeam_*`, `awayteam_*`, label `winner_is_home_team` (SQLite stores booleans as 0/1).
- Dates are ISO strings in DB; always use `utils.sqlite_date_string` / `date_from_sqlite_string`.
- Team identifiers: `teamSlug` from NBA.com (e.g., `lakers`, `sixers`). Use lowercase.

## Workflows you’ll likely automate
- Populate DB for a season:
  - Call `put_dates_in_db(date_range(season_start, season_end))` to scrape missing dates and append to `games.db`.
- Generate training data:
  - `with sqlite3.connect('games.db') as conn: df = generate_training_data_for_season(conn, season_start, season_end)`
- Predict a matchup (pattern from notebook):
  - Build two team averages over the season, drop `gamesCount`, add `hometeam_`/`awayteam_` prefixes, then `model.predict(df)`.

## Gotchas (seen in code)
- Scrapy/Twisted: Never run crawler twice in same process. Always go through `scrape_games_to_csv` (spawns a new process).
- GUI return shape: `create_model_gui()` returns `(model, season_string)`. Some notebook cells refer to `params_dict['Season']`; treat the second return as the season key for the `nba_seasons` dict.
- Site structure drift: Spider asserts all stats present. If selectors break, update the JSON path or relax assertions.

## Extending safely
- Add a stat: update the stat set in the spider AND the list (order!) in `get_average_stats_over_period`; adjust Keras input shape; retrain.
- New data source: keep the `games` table schema and column prefixes consistent to avoid downstream breakage.
- Prefer adding helpers in `.py` modules and calling them from notebooks; keep notebooks thin.

## Examples
- Quick day scrape in Python (Windows PowerShell):
  - `python -c "from datetime import date; from game_data_ingest_scraping import scrape_games_to_csv; scrape_games_to_csv('output_data.csv',[date(2010,1,2)])"`
- DB populate (code): use `put_dates_in_db(date_range(season_start, season_end))` from `game_data_ingest`.

If anything here diverges from your intent, please note it in PRs so we can fix the guide.
