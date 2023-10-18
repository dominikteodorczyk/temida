from utils.sports import ScrapersDict
from utils.events import MainEventsBoard
from threading import Thread
from queue import Queue


class ScrapersPool:
    """
    A class representing a pool of scrapers for collecting sports betting data.

    Attributes:
    -----------
    - sport (str): The sport for which the data is being collected.
    - bet_type (str): The type of bet for which the data is being collected.
    - data (MainEventsBoard): An instance of MainEventsBoard to store and
        manage the collected data.

    Parameters:
    -----------
    - sport (str): The sport for which the data is being collected.
    - bet_type (str): The type of bet for which the data is being collected.
    """

    def __init__(self, sport, bet_type) -> None:
        self.sport = sport
        self.bet_type = bet_type
        self.data = MainEventsBoard()

    def get_scrapers(self) -> dict:
        """
        Get the scrapers associated with the specified sport and bet type.

        Returns:
        --------
        dict: A dictionary containing scrapers for the specified sport and
            bet type. The keys are dynamically generated based on the sport,
            and the values are the corresponding scrapers.
        """
        srcapers: dict = {}
        for key, value in ScrapersDict().scrapers.items():
            srcapers[getattr(key, self.sport)] = value[self.bet_type - 2]
        return srcapers

    def get_data(self):
        """
        Retrieve data from multiple scrapers and update the MainEventsBoard.

        This method initializes threads for each scraper, collects the
        results in a queue, and updates the MainEventsBoard with the
        obtained data.
        """
        scrapers = self.get_scrapers()
        result_queue = Queue()
        threads = []

        for site_path, scraper in scrapers.items():
            thread = Thread(
                target=scraper.init_with(site_path).get_events_values,
                args=(result_queue,),
            )
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()

        while not result_queue.empty():
            self.data.put_data(result_queue.get())
