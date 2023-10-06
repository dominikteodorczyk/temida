from utils.parsers import *
import pytest
from datetime import datetime


class Test_Parser:
    @pytest.fixture
    def example_data(self):
        return {
            "home_player": "Galatasaray - Bayern M.",
            "away_player": "Galatasaray - Bayern M.",
            "home_team_win": "5,8",
            "draw": "4,8",
            "away_team_win": "1,47",
            "event_date": "12.09",
        }

    @pytest.fixture
    def expected_return(self):
        return {
            "home_player": "GALATASARAY",
            "away_player": "BAYERN M.",
            "home_team_win": 5.8,
            "draw": 4.8,
            "away_team_win": 1.47,
            "event_date": "2023-09-12",
        }

    def test_parse_home_win_return_float(self, example_data):
        parser = Parser()
        value = parser.parse_home_win(example_data["home_team_win"])
        assert type(value) is float

    def test_parse_home_win_return_proper_value(
        self, example_data, expected_return
    ):
        parser = Parser()
        value = parser.parse_home_win(example_data["home_team_win"])
        assert value == expected_return["home_team_win"]

    def test_parse_draw_return_float(self, example_data):
        parser = Parser()
        value = parser.parse_home_win(example_data["draw"])
        assert type(value) is float

    def test_parse_draw_return_proper_value(
        self, example_data, expected_return
    ):
        parser = Parser()
        value = parser.parse_home_win(example_data["draw"])
        assert value == expected_return["draw"]

    def test_parse_away_win_return_float(self, example_data):
        parser = Parser()
        value = parser.parse_home_win(example_data["away_team_win"])
        assert type(value) is float

    def test_parse_away_win_return_proper_value(
        self, example_data, expected_return
    ):
        parser = Parser()
        value = parser.parse_home_win(example_data["away_team_win"])
        assert value == expected_return["away_team_win"]


class Test_FortunaParser:
    @pytest.fixture
    def example_data(self):
        return {
            "home_player": "Galatasaray - Bayern M.",
            "away_player": "Galatasaray - Bayern M.",
            "home_team_win": "5,8",
            "draw": "4,8",
            "away_team_win": "1,47",
            "event_date": "12.12",
        }

    @pytest.fixture
    def expected_return(self):
        return {
            "event_name": "Galatasaray - Bayern M.",
            "home_player": "GALATASARAY",
            "away_player": "BAYERN M.",
            "home_team_win": 5.8,
            "draw": 4.8,
            "away_team_win": 1.47,
            "event_date": datetime.strptime(
                f"12.12.{datetime.now().year}", "%d.%m.%Y"
            ).date(),
        }

    @pytest.fixture
    def secound_example_date(self):
        return "01.01"

    @pytest.fixture
    def expected_return_date(self):
        return datetime.strptime(
            f"01.01.{datetime.now().year + 1}", "%d.%m.%Y"
        ).date()

    def test_parse_date_return_datetime(self, example_data, expected_return):
        parser = FortunaParser()
        value = parser.parse_date(example_data["event_date"])
        assert type(value) == type(expected_return["event_date"])

    def test_parse_date_return_proper_datetime(
        self, example_data, expected_return
    ):
        parser = FortunaParser()
        value = parser.parse_date(example_data["event_date"])
        assert value == expected_return["event_date"]

    def test_parse_date_return_proper_date_for_event_from_next_y(
        self, secound_example_date, expected_return_date
    ):
        parser = FortunaParser()
        value = parser.parse_date(secound_example_date)
        assert value == expected_return_date

    def test_parse_event_name_return_proper_str(
        self, example_data, expected_return
    ):
        parser = FortunaParser()
        value = parser.parse_event_name(
            example_data["home_player"], example_data["away_player"]
        )
        assert type(value) == str
        assert value == expected_return["event_name"]

    def test_parse_home_name_return_proper_str(
        self, example_data, expected_return
    ):
        parser = FortunaParser()
        value = parser.parse_home_name(example_data["home_player"])
        assert type(value) == str
        assert value == expected_return["home_player"]

    def test_parse_away_name_return_proper_str(
        self, example_data, expected_return
    ):
        parser = FortunaParser()
        value = parser.parse_away_name(example_data["away_player"])
        assert type(value) == str
        assert value == expected_return["away_player"]


class Test_STSParser:
    @pytest.fixture
    def example_data(self):
        return {
            "home_player": "Galatasaray ",
            "away_player": " Bayern M.",
            "home_team_win": "5,8",
            "draw": "4,8",
            "away_team_win": "1,47",
            "event_date": "12.12.2023",
        }

    @pytest.fixture
    def expected_return(self):
        return {
            "event_name": "Galatasaray - Bayern M.",
            "home_player": "GALATASARAY",
            "away_player": "BAYERN M.",
            "home_team_win": 5.8,
            "draw": 4.8,
            "away_team_win": 1.47,
            "event_date": datetime.strptime(f"12.12.2023", "%d.%m.%Y").date(),
        }

    @pytest.fixture
    def secound_example_date(self):
        return "Dzisiaj"

    @pytest.fixture
    def expected_return_date(self):
        return datetime.now().strftime("%Y-%m-%d")

    def test_parse_date_return_datetime(self, example_data, expected_return):
        parser = STSParser()
        value = parser.parse_date(example_data["event_date"])
        assert type(value) == type(expected_return["event_date"])

    def test_parse_date_return_proper_datetime(
        self, example_data, expected_return
    ):
        parser = STSParser()
        value = parser.parse_date(example_data["event_date"])
        assert value == expected_return["event_date"]

    def test_parse_date_return_proper_date_for_event_from_today_str(
        self, secound_example_date, expected_return_date
    ):
        parser = STSParser()
        value = parser.parse_date(secound_example_date)
        assert value == expected_return_date

    def test_parse_event_name_return_proper_str(
        self, example_data, expected_return
    ):
        parser = STSParser()
        value = parser.parse_event_name(
            example_data["home_player"], example_data["away_player"]
        )
        assert type(value) == str
        assert value == expected_return["event_name"]

    def test_parse_home_name_return_proper_str(
        self, example_data, expected_return
    ):
        parser = STSParser()
        value = parser.parse_home_name(example_data["home_player"])
        assert type(value) == str
        assert value == expected_return["home_player"]

    def test_parse_away_name_return_proper_str(
        self, example_data, expected_return
    ):
        parser = STSParser()
        value = parser.parse_away_name(example_data["away_player"])
        assert type(value) == str
        assert value == expected_return["away_player"]


class Test_BetclicParser:
    @pytest.fixture
    def example_data(self):
        return {
            "home_player": "Galatasaray ",
            "away_player": " Bayern M.",
            "home_team_win": "5,8",
            "draw": "4,8",
            "away_team_win": "1,47",
            "event_date": "12.12.2023",
        }

    @pytest.fixture
    def expected_return(self):
        return {
            "event_name": "Galatasaray - Bayern M.",
            "home_player": "GALATASARAY",
            "away_player": "BAYERN M.",
            "home_team_win": 5.8,
            "draw": 4.8,
            "away_team_win": 1.47,
            "event_date": datetime.strptime(f"12.12.2023", "%d.%m.%Y").date(),
        }

    @pytest.fixture
    def today_example_date(self):
        return "Dzisiaj"

    @pytest.fixture
    def expected_return_date(self):
        return datetime.now().strftime("%Y-%m-%d")

    @pytest.fixture
    def tomorrow_example_date(self):
        return "Jutro"

    @pytest.fixture
    def expected_return_tomorrow_date(self):
        return (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")

    @pytest.fixture
    def day_after_tomorrow_example_date(self):
        return "Pojutrze"

    @pytest.fixture
    def expected_return_day_after_tomorrow_date(self):
        return (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d")

    def test_parse_date_return_datetime(self, example_data, expected_return):
        parser = BetclicParser()
        value = parser.parse_date(example_data["event_date"])
        assert type(value) == type(expected_return["event_date"])

    def test_parse_date_return_proper_datetime(
        self, example_data, expected_return
    ):
        parser = BetclicParser()
        value = parser.parse_date(example_data["event_date"])
        assert value == expected_return["event_date"]

    def test_parse_date_return_proper_date_for_event_from_today_str(
        self, today_example_date, expected_return_date
    ):
        parser = BetclicParser()
        value = parser.parse_date(today_example_date)
        assert value == expected_return_date

    def test_parse_date_return_proper_date_for_tomorrow_str(
        self, tomorrow_example_date, expected_return_tomorrow_date
    ):
        parser = BetclicParser()
        value = parser.parse_date(tomorrow_example_date)
        assert value == expected_return_tomorrow_date

    def test_parse_date_return_proper_date_for_day_after_tmr_example_date_str(
        self,
        day_after_tomorrow_example_date,
        expected_return_day_after_tomorrow_date,
    ):
        parser = BetclicParser()
        value = parser.parse_date(day_after_tomorrow_example_date)
        assert value == expected_return_day_after_tomorrow_date

    def test_parse_event_name_return_proper_str(
        self, example_data, expected_return
    ):
        parser = BetclicParser()
        value = parser.parse_event_name(
            example_data["home_player"], example_data["away_player"]
        )
        assert type(value) == str
        assert value == expected_return["event_name"]

    def test_parse_home_name_return_proper_str(
        self, example_data, expected_return
    ):
        parser = BetclicParser()
        value = parser.parse_home_name(example_data["home_player"])
        assert type(value) == str
        assert value == expected_return["home_player"]

    def test_parse_away_name_return_proper_str(
        self, example_data, expected_return
    ):
        parser = BetclicParser()
        value = parser.parse_away_name(example_data["away_player"])
        assert type(value) == str
        assert value == expected_return["away_player"]
