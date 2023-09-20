from pandas import DataFrame

class TwoWayBetEvent:

    def __init__(self) -> None:
        pass


class TwoWayBetEventsTable:

    def __init__(self) -> None:
        self.events_list = DataFrame(columns=[
            "home_player",
            "away_player",
            "home_team_win",
            "away_team_win",
            "event_date"
        ])

    def imput_event(self, event_data: dict):
        self.events_list._append({
        })