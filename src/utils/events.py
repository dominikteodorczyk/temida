"""
A module containing classes of objects representing events.
"""

from pandas import DataFrame


class TwoWayBetEvent:
    """
    The object of a single event obtained by scraping data
    at all bookmakers.
    """

    def __init__(self) -> None:
        pass


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
        self.event_bets_values = DataFrame(columns=[
            "bookmaker",
            "home",
            "away"
            ]
        )

    def __repr__(self) -> str:
        return f"{self.home_player}_&_{self.away_player}"

    def make_bets_table(self):
        """
        Method that retrieves data for an event from individual
        bookmaker tables.
        """
        pass