from pandas import DataFrame


class TwoWayBetEvent:
    def __init__(self) -> None:
        pass


class TwoWayBetEventsTable:
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
        self.events_list._append({})


class Event:
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
        pass
