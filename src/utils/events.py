"""
A module containing classes of objects representing events.
"""

from pandas import DataFrame


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
        self.events_list:list = []
        self.events_table =  DataFrame()

    def put_data(self, data):
        self.events_list.append(data)

