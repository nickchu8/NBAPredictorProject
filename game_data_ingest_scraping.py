from scrapy import crawler
from nba_games_scraper.nba_games_scraper.spiders.games_spider import GamesSpider
from twisted.internet import reactor
from multiprocessing import Process, Queue
import logging
from datetime import date
import pathlib


# From https://stackoverflow.com/a/43661172
def f(q, settings, spider_args):
    try:
        process = crawler.CrawlerProcess(settings)
        process.crawl(GamesSpider, *spider_args)
        process.start()
        q.put(None)
    except Exception as e:
        q.put(e)


def scrape_games_to_csv(output_file_path: str, dates: list[date]):
    """
    Truncate `output_file_path` and scrape the games from `dates`
    into `output_file_path`.
    Run in a background process to work around Scrapy's I/O backend
    Twisted not being re-runnable. (i.e. `scrape_games_to_csv` can be
    safely called multiple times, but the underlying Scrapy stuff has
    to happen in a new process each time.)
    """

    settings = dict(
        FEEDS={
            output_file_path: {"format": "csv"},
        },
        LOG_LEVEL=logging.INFO,
        REQUEST_FINGERPRINTER_IMPLEMENTATION="2.7",
    )
    q = Queue()
    p = Process(target=f, args=(q, settings, (dates,)))
    pathlib.Path(output_file_path).unlink(missing_ok=True)
    print("Starting crawl")
    p.start()
    result = q.get()
    if result is not None:
        raise result
    p.join()
    print("Finished crawl")
