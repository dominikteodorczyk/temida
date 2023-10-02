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

    def to_dataframe(self):
        data = {
            "Event Name": [self.event_name],
            "Home Team": [self.home_player],
            "Away Team": [self.away_player],
            "Date": [self.event_date],
            "Home Win": [self.home_team_win],
            "Away Win": [self.away_team_win],
        }
        return DataFrame(data)

    @classmethod
    def create_from_data(cls, bukmacher_data, parser):
        home_player = parser.parse_home_name(bukmacher_data.get["home_team"])
        away_player = parser.parse_away_name(bukmacher_data.get["away_team"])
        event_name = parser.parse_event_name(
            bukmacher_data.get("home_team", "away_team")
        )
        event_date = parser.parse_date(bukmacher_data["date"])
        home_team_win = parser.parse_home_win(bukmacher_data["home_win"])
        away_team_win = parser.parse_away_win(bukmacher_data["away_win"])
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

    def to_dataframe(self):
        data = {
            "Event Name": [self.event_name],
            "Home Team": [self.home_player],
            "Away Team": [self.away_player],
            "Date": [self.event_date],
            "Home Win": [self.home_team_win],
            "Draw": [self.draw],
            "Away Win": [self.away_team_win],
        }
        return DataFrame(data)

    @classmethod
    def create_from_data(cls, bukmacher_data, parser):
        home_player = parser.parse_home_name(bukmacher_data.get["home_team"])
        away_player = parser.parse_away_name(bukmacher_data.get["away_team"])
        event_name = parser.parse_event_name(
            bukmacher_data.get("home_team", "away_team")
        )
        event_date = parser.parse_date(bukmacher_data["date"])
        home_team_win = parser.parse_home_win(bukmacher_data["home_win"])
        draw = parser.parse_draw(bukmacher_data["draw"])
        away_team_win = parser.parse_away_win(bukmacher_data["away_win"])
        return cls(
            event_name,
            home_player,
            away_player,
            event_date,
            home_team_win,
            draw,
            away_team_win,
        )


class TwoWayBetEventsTable:
    """
    Table of events obtained when scratching a given sport
    at a single bookmaker.
    """

    def __init__(self) -> None:
        self.events_list = DataFrame(
            columns=[
                "home_player",
                "away_player",
                "home_team_win",
                "away_team_win",
                "event_date",
            ]
        )

    def imput_event(self, event_data: dict):
        """
        Method of adding event objects when condensing all events
        of a given sport at a given bookmaker into a table.
        """
        self.events_list._append({})


class Event:
    """
    Values of odds for a given event at all bookmakers.
    """

    def __init__(self, home_player, away_player) -> None:
        self.home_player = home_player
        self.away_player = away_player
        self.event_bets_values = DataFrame(
            columns=["bookmaker", "home", "away"]
        )

    def __repr__(self) -> str:
        return f"{self.home_player}_&_{self.away_player}"

    def make_bets_table(self):
        """
        Method that retrieves data for an event from individual
        bookmaker tables.
        """
        pass
