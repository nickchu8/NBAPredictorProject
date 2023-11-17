from scrapy.crawler import CrawlerProcess
from nba_games_scraper.nba_games_scraper.spiders.games_spider import GamesSpider
import logging
from scrapy.utils.log import configure_logging
from datetime import date

process = CrawlerProcess(
    settings={
        "FEEDS": {
            "games-2000-01.csv": {"format": "csv"},
        },
        "LOG_LEVEL": logging.WARNING,
    }
)

process.crawl(GamesSpider, begin_date=date(2000, 1, 1), end_date=date(2000, 1, 31))
print("Starting crawl")
process.start()
print("Finished crawl")
