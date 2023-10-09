"""
A module containing classes of objects representing events.
"""

from pandas import DataFrame, Series
from copy import deepcopy
from numpy import nan


class BetEvent:
    def __init__(
        self, event_name, home_player, away_player, event_date
    ) -> None:
        self.event_name = event_name
        self.home_player = home_player
        self.away_player = away_player
        self.event_date = event_date


class TwoWayBetEvent(BetEvent):
    """
    The object of a single two-way event obtained by scraping data
    at all bookmakers.
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


# Przykład użycia
class ThreeWayBetEvent(BetEvent):
    """
    The object of a single three-way event obtained by scraping data
    at all bookmakers.
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
    def __init__(self, bookmaker) -> None:
        self.bookmaker = bookmaker
        self.data = DataFrame(
            columns=["event_name", "home_player", "away_player", "event_date"]
        )

    def __str__(self) -> str:
        return f"{self.bookmaker}"


class TwoWayBetEventsTable(BetEventsTable):
    """
    Table of events obtained when scratching a given sport
    at a single bookmaker.
    """

    def __init__(self, bookmaker) -> None:
        super().__init__(bookmaker)
        self.data["home_team_win"] = []
        self.data["away_team_win"] = []

    def put(self, event_data: object):
        """
        Method of adding event objects when condensing all events
        of a given sport at a given bookmaker into a table.
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
    Table of events obtained when scratching a given sport
    at a single bookmaker.
    """

    def __init__(self, bookmaker) -> None:
        super().__init__(bookmaker)
        self.data["home_team_win"] = []
        self.data["draw"] = []
        self.data["away_team_win"] = []

    def put(self, event_data: object):
        """
        Method of adding event objects when condensing all events
        of a given sport at a given bookmaker into a table.
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
    Values of odds for a given event at all bookmakers.
    """

    def __init__(self) -> None:
        self.events_dict: dict = {}
        self.events_table = DataFrame()

    def put_data(self, data):
        self.events_dict[data.__str__()] = data

    def get_cols_names(self):
        cols_list = []
        for key,value in self.events_dict.items():
            cols_list.append(key)
        return cols_list

    def get_unique_dates(self):
        date_list = []
        for key, events_object in self.events_dict.items():
            events_dates = events_object.data["event_date"].to_list()
            for date in events_dates:
                date_list.append(date)
        return list(set(date_list))

    def create_provisor_dict(self, date):
        provisor_events_list = {}
        for key, events_object in self.events_dict.items():
            events_names = events_object.data.loc[
                events_object.data["event_date"] == date, "event_name"
            ]
            provisor_events_list[key] = events_names.to_list()
        return provisor_events_list

    def highest_number_of_records(self, data):
        return max(data, key=lambda k: len(data[k]))

    def jaccard_similarity(self, s1, s2):
        set1 = set(s1)
        set2 = set(s2)
        intersection = len(set1.intersection(set2))
        union = len(set1) + len(set2) - intersection
        similarity = intersection / union
        return similarity

    def create_events_table(self):
        self.events_table = DataFrame(columns=self.get_cols_names())
        dates_list = self.get_unique_dates()
        for date in dates_list:
            work_dict = self.create_provisor_dict(date)
            main_list = work_dict[self.highest_number_of_records(work_dict)]
            rest_dict = deepcopy(work_dict)
            del rest_dict[self.highest_number_of_records(work_dict)]
            for main_event in main_list:
                temporal_dict = {}
                for key, value in rest_dict.items():
                    ratio = 0
                    best = None
                    for secound_event in value:
                        try:
                            similarity = self.jaccard_similarity(
                                main_event, secound_event
                            )
                            if similarity > 0.75:
                                if similarity > ratio:
                                    best = secound_event
                                    ratio = similarity
                        except:
                            best = None
                            pass
                    temporal_dict[key] = best
                temporal_dict[
                    self.highest_number_of_records(work_dict)
                ] = main_event
                self.events_table = self.events_table._append(
                    temporal_dict, ignore_index=True
                )
        mask = self.events_table.count(axis=1) == 1
        self.events_table = self.events_table[~mask]
        return self.events_table


class Event:

    def __init__(self,events_data) -> None:
        self.events_data:dict = events_data

    @classmethod
    def create(cls, event_row: Series,events_dict):
        events_data = {}
        for key, value in event_row.to_dict().items():
            if type(value) == str:
                data_frame = events_dict[key]
                events_data[key] = data_frame.data.loc[data_frame.data['event_name']==value]
        return cls(events_data)
    



        
    

    
