# to run:
# $ scrapy crawl games_spider -o games-2010-01.csv

import scrapy
import json
from datetime import datetime, date, timedelta


class GamesSpider(scrapy.Spider):
    name = "games_spider"
    allowed_domains = ["www.nba.com"]

    def __init__(
        self, date_begin=date(2010, 1, 1), date_end=date(2010, 1, 31), *args, **kwargs
    ):
        super().__init__(*args, **kwargs)
        assert date_begin <= date_end
        ndays = int((date_end - date_begin).days)
        deltas = (timedelta(n) for n in range(ndays + 1))
        self.start_urls = [
            f"https://www.nba.com/games?date={date_begin + d}" for d in deltas
        ]

    def parse(self, response):
        """
        Handles a page with a URL of the form https://www.nba.com/games?date=yyyy-mm-dd.
        Follows the URLs to each game on that day with a callback of parse_game().
        """
        for game_url in response.css('a[data-text="GAME DETAILS"]::attr(href)'):
            yield response.follow(game_url, callback=self.parse_game)

    def parse_game(self, response):
        """
        Handles a page with a URL of the form https://www.nba.com/games?was-vs-dal-0011000010.
        Yields one dict with data about that game: date & time, home and away teams, statistics on
        those teams' performance, and who won the game.
        """
        data_json = response.xpath('//script[@id="__NEXT_DATA__"]/text()').get()
        game = json.loads(data_json)["props"]["pageProps"]["game"]
        home_team_won = game["homeTeam"]["score"] > game["awayTeam"]["score"]

        relevant_stats = {
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
        }

        home_team_stats = {
            ("hometeam_" + k): v
            for k, v in game["homeTeam"]["statistics"].items()
            if k in relevant_stats
        }

        away_team_stats = {
            ("awayteam_" + k): v
            for k, v in game["awayTeam"]["statistics"].items()
            if k in relevant_stats
        }

        # Ensure that we have every field we came for, to avoid feeding the model incomplete data
        assert len(home_team_stats) == len(relevant_stats)
        assert len(away_team_stats) == len(relevant_stats)

        game_info = dict(
            datetime_utc=datetime.fromisoformat(game["gameTimeUTC"]),
            hometeam_slug=game["homeTeam"]["teamSlug"],
            awayteam_slug=game["awayTeam"]["teamSlug"],
            winner_is_home_team=home_team_won,
        )
        yield game_info | home_team_stats | away_team_stats
