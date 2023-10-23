"""
Module events:

Module containing classes for representing and managing betting events.

Classes:
--------
1. BetEvent: Base class for representing a betting event.
2. TwoWayBetEvent: Subclass of BetEvent, representing a two-way
    betting event.
3. ThreeWayBetEvent: Subclass of BetEvent, representing a three-way
    betting event.
4. BetEventsTable: Class for managing a table of betting events.
5. TwoWayBetEventsTable: Subclass of BetEventsTable, managing tables for
    two-way events.
6. ThreeWayBetEventsTable: Subclass of BetEventsTable, managing tables
    for three-way events.
7. MainEventsBoard: Class representing the main board containing various
    bettings for event.
8. Event: Class representing a specific sports betting event.
"""

from typing import List, Dict
from copy import deepcopy
from threading import Thread
from queue import Queue
from pandas import DataFrame, Series
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import AgglomerativeClustering
from utils.technical import Constant


class BetEvent:
    """
    BetEvent - Base class for representing a betting event.

    Attributes:
    -----------
    - event_name (str): The name of the betting event.
    - home_player (str): The name of the home player or team.
    - away_player (str): The name of the away player or team.
    - event_date (str): The date of the betting event.
    """

    def __init__(
        self, event_name, home_player, away_player, event_date
    ) -> None:
        self.event_name = event_name
        self.home_player = home_player
        self.away_player = away_player
        self.event_date = event_date


class TwoWayBetEvent(BetEvent):
    """
    Represents a single two-way betting event obtained by scraping data
    from all bookmakers.

    Inherits from BetEvent.

    Attributes:
    - home_team_win (float): The odds for the home team to win.
    - away_team_win (float): The odds for the away team to win.

    Parameters:
    - event_name (str): The name of the betting event.
    - home_player (str): The name of the home player or team.
    - away_player (str): The name of the away player or team.
    - event_date (str): The date of the betting event.
    - home_team_win (float): The odds for the home team to win.
    - away_team_win (float): The odds for the away team to win.
    """

    def __init__(
        self,
        event_name,
        home_player,
        away_player,
        event_date,
        home_team_win,
        away_team_win,
    ) -> None:
        super().__init__(
            event_name,
            home_player,
            away_player,
            event_date,
        )
        self.home_team_win = home_team_win
        self.away_team_win = away_team_win

    @classmethod
    def create_from_data(cls, bukmacher_data, parser):
        """
        Creates a TwoWayBetEvent instance from scraped data using a parser.

        Parameters:
        - bukmacher_data (dict): A dictionary containing scraped data from
            a bookmaker.
        - parser: An instance of the parser used for data extraction.

        Returns:
        - TwoWayBetEvent: An instance of the TwoWayBetEvent class created
            from the provided data.
        """
        home_player = parser.parse_home_name(bukmacher_data["home_player"])
        away_player = parser.parse_away_name(bukmacher_data["away_player"])
        event_name = parser.parse_event_name(
            bukmacher_data["home_player"], bukmacher_data["away_player"]
        )
        event_date = parser.parse_date(bukmacher_data["event_date"])
        home_team_win = parser.parse_home_win(bukmacher_data["home_team_win"])
        away_team_win = parser.parse_away_win(bukmacher_data["away_team_win"])
        return cls(
            event_name,
            home_player,
            away_player,
            event_date,
            home_team_win,
            away_team_win,
        )


class ThreeWayBetEvent(BetEvent):
    """
    Represents a single three-way betting event obtained by scraping
    data from all bookmakers.

    Inherits from BetEvent.

    Attributes:
    - home_team_win (float): The odds for the home team to win.
    - draw (float): The odds for a draw.
    - away_team_win (float): The odds for the away team to win.

    Parameters:
    - event_name (str): The name of the betting event.
    - home_player (str): The name of the home player or team.
    - away_player (str): The name of the away player or team.
    - event_date (str): The date of the betting event.
    - home_team_win (float): The odds for the home team to win.
    - draw (float): The odds for a draw.
    - away_team_win (float): The odds for the away team to win.
    """

    def __init__(
        self,
        event_name,
        home_player,
        away_player,
        event_date,
        home_team_win,
        draw,
        away_team_win,
    ) -> None:
        super().__init__(event_name, home_player, away_player, event_date)
        self.home_team_win = home_team_win
        self.away_team_win = away_team_win
        self.draw = draw

    @classmethod
    def create_from_data(cls, bukmacher_data, parser):
        """
        Creates a ThreeWayBetEvent instance from scraped data using a parser.

        Parameters:
        - bukmacher_data (dict): A dictionary containing scraped data from a
            bookmaker.
        - parser: An instance of the parser used for data extraction.

        Returns:
        - ThreeWayBetEvent: An instance of the ThreeWayBetEvent class created
            from the provided data.
        """
        home_player = parser.parse_home_name(bukmacher_data["home_player"])
        away_player = parser.parse_away_name(bukmacher_data["away_player"])
        event_name = parser.parse_event_name(
            bukmacher_data["home_player"], bukmacher_data["away_player"]
        )
        event_date = parser.parse_date(bukmacher_data["event_date"])
        home_team_win = parser.parse_home_win(bukmacher_data["home_team_win"])
        draw = parser.parse_draw(bukmacher_data["draw"])
        away_team_win = parser.parse_away_win(bukmacher_data["away_team_win"])
        return cls(
            event_name,
            home_player,
            away_player,
            event_date,
            home_team_win,
            draw,
            away_team_win,
        )


class BetEventsTable:
    """
    Represents a table of betting events for a specific bookmaker.

    Attributes:
    - bookmaker (str): The name or identifier of the bookmaker.
    - data (DataFrame): A pandas DataFrame containing information about
        betting events.

    Parameters:
    - bookmaker (str): The name or identifier of the bookmaker.
    """

    def __init__(self, bookmaker) -> None:
        self.bookmaker = bookmaker
        self.data = DataFrame(
            columns=["event_name", "home_player", "away_player", "event_date"]
        )

    def __str__(self) -> str:
        """
        Returns a string representation of the BetEventsTable.

        Returns:
        - str: A string representation of the BetEventsTable.
        """
        return f"{self.bookmaker}"


class TwoWayBetEventsTable(BetEventsTable):
    """
    Table of events obtained when scraping a given sport
    at a single bookmaker.

    Attributes:
    - Inherits from BetEventsTable.

    Parameters:
    - bookmaker (str): The name or identifier of the bookmaker.
    """

    def __init__(self, bookmaker) -> None:
        super().__init__(bookmaker)
        self.data["home_team_win"] = []
        self.data["away_team_win"] = []

    def put(self, event_data: object):
        """
        Adds event objects when consolidating all events of a given sport
        at a given bookmaker into a table.

        Parameters:
        - event_data (object): An instance of TwoWayBetEvent containing
            event data.
        """
        self.data = self.data._append(
            {
                "event_name": event_data.event_name,
                "home_player": event_data.home_player,
                "away_player": event_data.away_player,
                "event_date": event_data.event_date,
                "home_team_win": event_data.home_team_win,
                "away_team_win": event_data.away_team_win,
            },
            ignore_index=True,
        )


class ThreeWayBetEventsTable(BetEventsTable):
    """
    Table of events obtained when scraping a given sport
    at a single bookmaker.

    Attributes:
    - Inherits from BetEventsTable.

    Parameters:
    - bookmaker (str): The name or identifier of the bookmaker.
    """

    def __init__(self, bookmaker) -> None:
        super().__init__(bookmaker)
        self.data["home_team_win"] = []
        self.data["draw"] = []
        self.data["away_team_win"] = []

    def put(self, event_data: object):
        """
        Adds event objects when consolidating all events of a given sport
        at a given bookmaker into a table.

        Parameters:
        - event_data (object): An instance of ThreeWayBetEvent containing
            event data.
        """
        self.data = self.data._append(
            {
                "event_name": event_data.event_name,
                "home_player": event_data.home_player,
                "away_player": event_data.away_player,
                "event_date": event_data.event_date,
                "home_team_win": event_data.home_team_win,
                "draw": event_data.draw,
                "away_team_win": event_data.away_team_win,
            },
            ignore_index=True,
        )


class MainEventsBoard:
    """
    Represents the values of odds for a given event at all bookmakers.

    Attributes:
    -----------
    - events_dict (dict): A dictionary containing data frames for
        different bookmakers.
    - events_table (pandas.DataFrame): A data frame containing odds
        values for events.

    Parameters:
    -----------
    - bookmaker (str): The name of the bookmaker.
    - events_table (TwoWayBetEventsTable or ThreeWayBetEventsTable):
        The event table for the bookmaker.
    """

    def __init__(self) -> None:
        self.events_dict: dict = {}
        self.events_table = DataFrame()

    def put_data(
        self, data: TwoWayBetEventsTable or ThreeWayBetEventsTable
    ) -> None:
        """
        Adds a bookmaker's event table to the MainEventsBoard.

        Parameters:
        -----------
        data (TwoWayBetEventsTable or ThreeWayBetEventsTable):
            The event table for the bookmaker.
        """
        self.events_dict[data.__str__()] = data

    def get_cols_names(self) -> List[str]:
        """
        Retrieves the column names representing different bookmakers.

        Returns:
        --------
        List[str]: A list of column names representing different bookmakers.
        """
        cols_list = []
        for key, value in self.events_dict.items():
            cols_list.append(key)
        return cols_list

    def get_unique_dates(self) -> List[str]:
        """
        Get a list of unique dates from all events in the MainEventsBoard.

        Returns:
        --------
        List[str]: A list containing unique dates from all events.
        """
        date_list = []
        for key, events_object in self.events_dict.items():
            date_list.extend(events_object.data["event_date"].to_list())
        return list(set(date_list))

    def create_provisor_dict(self, date: str) -> Dict[str, List[str]]:
        """
        Create a provisional dictionary mapping bookmakers to lists
        of event names for a given date.

        Parameters:
        -----------
        - date (str): The date for which the provisional dictionary
            is created.

        Returns:
        --------
        Dict[str, List[str]]: A dictionary where keys are bookmakers,
        and values are lists of event names for the specified date.
        """
        provisor_events_list = {}
        for key, events_object in self.events_dict.items():
            events_names = events_object.data.loc[
                events_object.data["event_date"] == date, "event_name"
            ]
            provisor_events_list[key] = events_names.to_list()
        return provisor_events_list

    def highest_number_of_records(self, data: Dict[str, List[str]]) -> str:
        """
        Find the bookmaker with the highest number of records.

        Parameters:
        -----------
        - data (Dict[str, List[str]]): A dictionary where keys are bookmakers,
        and values are lists of records.

        Returns:
        --------
        str: The bookmaker with the highest number of records.
        """
        return max(data, key=lambda k: len(data[k]))

    def jaccard_similarity(self, first_string, secound_string) -> float:
        """
        Calculate the Jaccard similarity between two sets.

        Parameters:
        -----------
        - first_string (str): First set or iterable.
        - secound_string (str): Second set or iterable.

        Returns:
        --------
        float: Jaccard similarity between the two sets.
        """
        set1 = set(first_string)
        set2 = set(secound_string)
        union = len(set1) + len(set2) - len(set1.intersection(set2))
        return len(set1.intersection(set2)) / union

    def cluster_strings(self, string_list) -> Dict[int, List[int]]:
        """
        Cluster strings using hierarchical agglomerative clustering
        based on TF-IDF vectors.

        Parameters:
        -----------
        - string_list (List[Iterable[str]]): List of iterables, each containing
            strings to be clustered.

        Returns:
        --------
        Dict[int, List[int]]: A dictionary where keys are cluster labels
        and values are lists of indices corresponding to the input lists.
        """
        vectorizer = TfidfVectorizer()
        X = vectorizer.fit_transform([" ".join(lst) for lst in string_list])
        clustering = AgglomerativeClustering(
            n_clusters=None,
            distance_threshold=Constant.CLUSTER_STRINGS_THRESHOLDS,
            linkage="average",
            metric="cosine",
        )
        labels = clustering.fit_predict(X.toarray())

        clusters = {}
        for idx, label in enumerate(labels):
            if label not in clusters:
                clusters[label] = []
            clusters[label].append(idx)

        return clusters

    def run_matching_pool(self, main_event, other_events_dict) -> dict:
        """
        Run a matching pool to find matching events.

        Parameters:
        -----------
        main_event (str): The main event for which matches are sought.
        other_events_dict (dict): A dictionary containing events to match against.

        Returns:
        --------
        dict: A dictionary containing matching events.
        """
        matching_events_dict = {}
        result_queue = Queue()
        slots = []
        results = []
        for key, value in other_events_dict.items():
            thread = Thread(
                target=self.find_matching_events_jaccard,
                args=(
                    key,
                    value,
                    main_event,
                    result_queue,
                ),
            )
            thread.start()
            slots.append(thread)

        for slot in slots:
            slot.join()
        while not result_queue.empty():
            results.append(result_queue.get())

        for match in results:
            matching_events_dict[match[0]] = match[1]

        return matching_events_dict

    def find_matching_events_cluster(
        self, key, value, main_event, result_queue
    ):
        """
        Find matching events based on clustering.

        Parameters:
        -----------
        key (str): The key of the event in the dictionary.
        value (list): The list of events to match against.
        main_event (str): The main event for which matches are sought.
        result_queue (Queue): A queue to store the results.
        """
        best_match = None
        for second_event in value:
            events_list = [[main_event], [second_event]]
            similarity = self.cluster_strings(events_list)
            if len(similarity) == 1:
                best_match = second_event
                # modification by removing the external
                # list object to speed up calculations
                value.remove(best_match)
        reuslt = (key, best_match)
        result_queue.put(reuslt)

    def find_matching_events_jaccard(
        self, key, value, main_event, result_queue
    ):
        """
        Find matching events based on Jaccard similarity.

        Parameters:
        -----------
        key (str): The key of the event in the dictionary.
        value (list): The list of events to match against.
        main_event (str): The main event for which matches are sought.
        result_queue (Queue): A queue to store the results.
        """
        # test method with lower accuracy but higher speed of calc.
        best_match = None
        ratio = 0
        for second_event in value:
            try:
                similarity = self.jaccard_similarity(main_event, second_event)
                if similarity > 0.6:
                    if similarity > ratio:
                        parts1 = [
                            part.strip() for part in main_event.split("-")
                        ]
                        parts2 = [
                            part.strip() for part in second_event.split("-")
                        ]
                        home_similarity = self.jaccard_similarity(
                            parts1[0], parts2[0]
                        )
                        away_similarity = self.jaccard_similarity(
                            parts1[1], parts2[1]
                        )
                        if (home_similarity > 0.5) and (away_similarity > 0.5):
                            best_match = second_event
                            ratio = similarity
            except:
                best_match = None

        # value.remove(best_match)
        reuslt = (key, best_match)
        result_queue.put(reuslt)

    def create_events_table(self) -> DataFrame:
        """
        Create an events table by clustering and matching events from
        different bookmakers.

        Returns:
        --------
        DataFrame: A DataFrame containing matched events from different
        bookmakers.
        """
        self.events_table = DataFrame(columns=self.get_cols_names())
        dates_list = self.get_unique_dates()
        for date in dates_list:
            work_dict = self.create_provisor_dict(date)
            main_bookmaker = self.highest_number_of_records(work_dict)
            main_events_dict = work_dict[main_bookmaker]
            other_events_dict = deepcopy(work_dict)
            del other_events_dict[main_bookmaker]
            for main_event in main_events_dict:
                matching_events_dict = self.run_matching_pool(
                    main_event, other_events_dict
                )
                matching_events_dict[main_bookmaker] = main_event
                self.events_table = self.events_table._append(
                    matching_events_dict, ignore_index=True
                )
        mask = self.events_table.count(axis=1) == 1
        self.events_table = self.events_table[~mask]
        return self.events_table


class Event:
    """
    Represents a sport betting event.

    Attributes:
    -----------
    - events_data (dict): A dictionary containing data frames for
        different bookmakers.
    """

    def __init__(self, events_data) -> None:
        self.events_data: dict = events_data

    @classmethod
    def create(cls, event_row: Series, events_dict) -> "Event":
        """
        Creates an instance of the Event class based on the provided event_row
        and events_dict.

        Parameters:
        -----------
        - cls (class): The class (Event) that this method belongs to.
        - event_row (pandas.Series): A row of data representing an event.
        - events_dict (dict): A dictionary containing data frames for different
            bookmakers.

        Returns:
        --------
        - Event: An instance of the Event class created based on the
            provided data.
        """
        events_data = {}
        for key, value in event_row.to_dict().items():
            if isinstance(value, str):
                data_frame = events_dict[key]
                events_data[key] = data_frame.data.loc[
                    data_frame.data["event_name"] == value
                ]
        return cls(events_data)
