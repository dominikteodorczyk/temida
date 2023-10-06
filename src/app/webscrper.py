from utils.sports import ScrapersDict
from utils.events import MainEventsBoard
from threading import Thread
from queue import Queue


class ScrapersPool:
    def __init__(self, sport, bet_type) -> None:
        self.sport = sport
        self.bet_type = bet_type

    def get_scrapers(self):
        srcapers: dict = {}
        for key, value in ScrapersDict().scrapers.items():
            srcapers[getattr(key, self.sport)] = value[self.bet_type - 2]
        return srcapers

    def get_data(self):
        scrapers = self.get_scrapers()
        results = MainEventsBoard().events_table
        result_queue = Queue()
        slots = []

        for site_path, scraper in scrapers.items():
            thread = Thread(
                target=scraper.init_with(site_path).get_events_values, args=(result_queue,))
            thread.start()
            slots.append(thread)

        for slot in slots:
            slot.join()
        while not result_queue.empty():
            results.append(result_queue.get())

        return results