from utils.parsers import *
import pytest
from datetime import datetime

class Test_Parser:

    @pytest.fixture
    def example_data(self):
        return {
            "home_player": 'Galatasaray - Bayern M.',
            "away_player": 'Galatasaray - Bayern M.',
            "home_team_win": '5,8',
            "draw": '4,8',
            "away_team_win": '1,47',
            "event_date": '12.09'
        }

    @pytest.fixture
    def expected_return(self):
        return {
            "home_player": 'GALATASARAY',
            "away_player": 'BAYERN M.',
            "home_team_win": 5.8,
            "draw": 4.8,
            "away_team_win": 1.47,
            "event_date": '2023-09-12'
        }

    def test_parse_home_win_return_float(self, example_data):
        parser = Parser()
        value = parser.parse_home_win(example_data["home_team_win"])
        assert type(value) is float

    def test_parse_home_win_return_proper_value(self, example_data,expected_return):
        parser = Parser()
        value = parser.parse_home_win(example_data["home_team_win"])
        assert value == expected_return["home_team_win"]

    def test_parse_draw_return_float(self, example_data):
        parser = Parser()
        value = parser.parse_home_win(example_data["draw"])
        assert type(value) is float

    def test_parse_draw_return_proper_value(self, example_data,expected_return):
        parser = Parser()
        value = parser.parse_home_win(example_data["draw"])
        assert value == expected_return["draw"]

    def test_parse_away_win_return_float(self, example_data):
        parser = Parser()
        value = parser.parse_home_win(example_data["away_team_win"])
        assert type(value) is float

    def test_parse_away_win_return_proper_value(self, example_data,expected_return):
        parser = Parser()
        value = parser.parse_home_win(example_data["away_team_win"])
        assert value == expected_return["away_team_win"]


class Test_FortunaParser:

    @pytest.fixture
    def example_data(self):
        return {
            "home_player": 'Galatasaray - Bayern M.',
            "away_player": 'Galatasaray - Bayern M.',
            "home_team_win": '5,8',
            "draw": '4,8',
            "away_team_win": '1,47',
            "event_date": '12.12'
        }

    @pytest.fixture
    def expected_return(self):
        return {
            "event_name": 'Galatasaray - Bayern M.',
            "home_player": 'GALATASARAY',
            "away_player": 'BAYERN M.',
            "home_team_win": 5.8,
            "draw": 4.8,
            "away_team_win": 1.47,
            "event_date": datetime.strptime(
                f"12.12.{datetime.now().year}", "%d.%m.%Y"
            ).date()
        }

    @pytest.fixture
    def secound_example_date(self):
        return '01.01'

    @pytest.fixture
    def expected_return_date(self):
        return datetime.strptime(
                f"01.01.{datetime.now().year + 1}", "%d.%m.%Y"
            ).date()

    def test_parse_date_return_datetime(self,example_data, expected_return):
        parser = FortunaParser()
        value = parser.parse_date(example_data["event_date"])
        assert type(value) == type(expected_return["event_date"])

    def test_parse_date_return_proper_datetime(self,example_data, expected_return):
        parser = FortunaParser()
        value = parser.parse_date(example_data["event_date"])
        assert value == expected_return["event_date"]

    def test_parse_date_return_proper_date_for_event_from_next_y(self,secound_example_date, expected_return_date):
        parser = FortunaParser()
        value = parser.parse_date(secound_example_date)
        assert value == expected_return_date

    def test_parse_event_name_return_str(self, example_data):
        parser = FortunaParser()
        value = parser.parse_event_name(example_data["home_player"],example_data["away_player"])
        assert type(value) == str