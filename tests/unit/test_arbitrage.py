import pytest
from unittest.mock import Mock
from utils.events import Event
from app.arbitrage import (
    ArbitrageCalculator,
    TwoWayArbitrageCalculator,
    ThreeWayArbitrageCalculator,
)
from pandas import DataFrame
from utils.technical import Constant


class Test_ArbitrageCalculator:
    """
    Test Class:
    ------------
    This class contains unit tests for the ArbitrageCalculator class methods.
    Each test method focuses on a specific functionality of the calculator.

    Notes:
    ------
    - The tests use a mocked event object to simulate event data.
    - Test data and specific values for calculations are provided in each method.
    - The results are checked against expected values to ensure accuracy.
    """
    @pytest.fixture
    def event_mock(self):
        return Mock(spec=Event)

    def test_get_probability(self, event_mock):
        """
        Test Case:
        ----------
        The method calculates the implied probability using the provided odds and
        verifies that the result is within an acceptable range of the expected
        probability.

        Steps:
        ------
        1. Create an ArbitrageCalculator instance with the mocked event.
        2. Call the get_probability method with a specified odds value (1.2).
        3. Check that the result, when rounded to two decimal places, matches the
        expected implied probability (0.93).
        """
        calculator = ArbitrageCalculator(event_mock)
        result = calculator.get_probability(1.2)
        assert round(result, 2) == 0.93

    def test_calculate_money_ratio(self, event_mock):
        """
        Test Case:
        ----------
        The method calculates the money ratio based on a given event probability
        and ensures that the result is within an acceptable range.

        Steps:
        ------
        1. Create an ArbitrageCalculator instance with the mocked event.
        2. Set a specific event probability (0.90).
        3. Call the calculate_money_ratio method with the provided probability.
        4. Check that the result, when rounded to two decimal places, matches the
        expected money ratio (1.11).
        """
        calculator = ArbitrageCalculator(event_mock)
        event_probability = 0.90
        result = calculator.calculate_money_ratio(event_probability)
        assert round(result, 2) == 1.11

    def test_calculate_return(self, event_mock):
        """
        Test Case:
        ----------
        The method calculates the potential return based on the provided stake
        amount and odds and ensures that the result is within an acceptable range.

        Steps:
        ------
        1. Create an ArbitrageCalculator instance with the mocked event.
        2. Set specific values for the stake amount (100.00) and odds (1.20).
        3. Call the calculate_return method with the provided money and odds.
        4. Check that the result, when rounded to two decimal places, matches the
        expected return (120.00).
        """
        calculator = ArbitrageCalculator(event_mock)
        money = 100.00
        odds = 1.20
        result = calculator.calculate_return(money=money, odds=odds)
        assert round(result, 2) == 120.00


class Test_TwoWayArbitrageCalculator:
    """
    Data containing 3-way orders were used for testing. This does not affect
    the results obtained, as data filtering and further calculations
    eliminate the use of draw information
    """

    @pytest.fixture
    def event_mock(self):
        events_data = {
            "STS": DataFrame(
                {
                    "event_name": "Karagumruk - Adana Demirspor",
                    "home_player": "KARAGUMRUKr",
                    "away_player": "ADANA DEMIRSPOR",
                    "event_date": "2023-10-23",
                    "home_team_win": 1.2,
                    "away_team_win": 1.2,
                },
                index=[0],
            ),
            "FORTUNA": DataFrame(
                {
                    "event_name": "Karagumruk - Adana Demirspor",
                    "home_player": "KARAGUMRUKr",
                    "away_player": "ADANA DEMIRSPOR",
                    "event_date": "2023-10-23",
                    "home_team_win": 1.2,
                    "away_team_win": 2.2,
                },
                index=[0],
            ),
            "BETCLIC": DataFrame(
                {
                    "event_name": "Karagumruk - Adana Demirspor",
                    "home_player": "KARAGUMRUKr",
                    "away_player": "ADANA DEMIRSPOR",
                    "event_date": "2023-10-23",
                    "home_team_win": 2.1,
                    "away_team_win": 1.2,
                },
                index=[0],
            ),
            "SUPERBET": DataFrame(
                {
                    "event_name": "Karagumruk - Adana Demirspor",
                    "home_player": "KARAGUMRUKr",
                    "away_player": "ADANA DEMIRSPOR",
                    "event_date": "2023-10-23",
                    "home_team_win": 1.2,
                    "away_team_win": 2.1,
                },
                index=[0],
            ),
        }
        mock_object = Mock(spec=Event)
        mock_object.events_data = events_data

        return mock_object

    @pytest.fixture
    def positive_event_mock_two_way(self):
        events_data = {
            "STS": DataFrame(
                {
                    "event_name": "Karagumruk - Adana Demirspor",
                    "home_player": "KARAGUMRUKr",
                    "away_player": "ADANA DEMIRSPOR",
                    "event_date": "2023-10-23",
                    "home_team_win": 2.9,
                    "away_team_win": 2.22,
                },
                index=[0],
            ),
            "FORTUNA": DataFrame(
                {
                    "event_name": "Karagumruk - Adana Demirspor",
                    "home_player": "KARAGUMRUKr",
                    "away_player": "ADANA DEMIRSPOR",
                    "event_date": "2023-10-23",
                    "home_team_win": 2.9,
                    "away_team_win": 2.2,
                },
                index=[0],
            ),
            "BETCLIC": DataFrame(
                {
                    "event_name": "Karagumruk - Adana Demirspor",
                    "home_player": "KARAGUMRUKr",
                    "away_player": "ADANA DEMIRSPOR",
                    "event_date": "2023-10-23",
                    "home_team_win": 2.95,
                    "away_team_win": 2.22,
                },
                index=[0],
            ),
            "SUPERBET": DataFrame(
                {
                    "event_name": "Karagumruk - Adana Demirspor",
                    "home_player": "KARAGUMRUKr",
                    "away_player": "ADANA DEMIRSPOR",
                    "event_date": "2023-10-23",
                    "home_team_win": 3.0,
                    "away_team_win": 2.25,
                },
                index=[0],
            ),
        }
        mock_object = Mock(spec=Event)
        mock_object.events_data = events_data

        return mock_object

    @pytest.fixture
    def expected_dataframe(self):
        return DataFrame(
            {
                "STS_index": 0,
                "STS_home_team_win": 2.9,
                "STS_away_team_win": 2.22,
                "FORTUNA_index": 0,
                "FORTUNA_home_team_win": 2.9,
                "FORTUNA_away_team_win": 2.2,
                "BETCLIC_index": 0,
                "BETCLIC_home_team_win": 2.95,
                "BETCLIC_away_team_win": 2.22,
                "SUPERBET_index": 0,
                "SUPERBET_home_team_win": 3.0,
                "SUPERBET_away_team_win": 2.25,
            },
            index=[0],
        )

    def test_create_data_source_return_dataframe(
        self, positive_event_mock_two_way, expected_dataframe
    ):
        calculator = TwoWayArbitrageCalculator(positive_event_mock_two_way)
        result = calculator.create_data_source()
        assert result.equals(expected_dataframe)

    def test_create_combinations_return_right_number_of_combinations(
        self, positive_event_mock_two_way
    ):
        calculator = TwoWayArbitrageCalculator(positive_event_mock_two_way)
        result = calculator.create_combinations()
        assert len(result) == 16

    def test_get_values_from_dict(self, event_mock):
        calculator = TwoWayArbitrageCalculator(event_mock)
        dictionary = {
            "STS_home_team_win": 2.9,
            "BETCLIC_away_team_win": 2.22,
        }
        expected_return = (2.9, 2.22)
        result = calculator.get_values_from_dict(dictionary)
        assert result == expected_return

    def test_calculate_implied_probability(self, event_mock):
        calculator = TwoWayArbitrageCalculator(event_mock)
        result = calculator.calculate_implied_probability(
            home_odds=2.9, away_odds=2.22
        )
        assert round(result, 2) == 0.89

    def test_calculate_odds_value(self, event_mock):
        calculator = TwoWayArbitrageCalculator(event_mock)
        result = calculator.calculate_odds_value(
            money_ratio=1.11, home_win=3.1, away_win=3.6
        )
        home_odds = (
            Constant.TEST_STAKE * ((1 + Constant.TAX_VALUE) / 3.1) * 1.11
        )
        away_odds = (
            Constant.TEST_STAKE * ((1 + Constant.TAX_VALUE) / 3.6) * 1.11
        )
        assert result == (home_odds, away_odds)

    def test_calculate_final_return(self, event_mock):
        calculator = TwoWayArbitrageCalculator(event_mock)
        home_win = 3.5
        home_money = 45.31
        away_money = 54.69
        result = calculator.calculate_final_return(
            home_money, home_win, away_money
        )
        assert round(result, 2) == 53.15

    def test_calculate_arbitrage_return_none_if_event_not_have_chanse(
        self, event_mock
    ):
        calculator = TwoWayArbitrageCalculator(event_mock)
        result = calculator.calculate_arbitrage()
        assert result == None

    def test_calculate_arbitrage_return_dict_in_list_if_event_have_chanse(
        self, positive_event_mock_two_way
    ):
        calculator = TwoWayArbitrageCalculator(positive_event_mock_two_way)
        result = calculator.calculate_arbitrage()
        assert len(result) == 16

    def test_calculate_arbitrage_return_dict_if_event_have_chanse(
        self, positive_event_mock_two_way
    ):
        calculator = TwoWayArbitrageCalculator(positive_event_mock_two_way)
        calculator.create_combinations = Mock(
            return_value=[
                {
                    "STS_home_team_win": 3.5,
                    "SUPERBET_away_team_win": 4.5,
                }
            ]
        )
        result = calculator.calculate_arbitrage()
        assert result == [
            {
                "STS_home_team_win": 3.5,
                "SUPERBET_away_team_win": 4.5,
            }
        ]

    def test_calculate_arbitrage_return_none_if_event_not_have_chanse_second(
        self, positive_event_mock_two_way
    ):
        calculator = TwoWayArbitrageCalculator(positive_event_mock_two_way)
        calculator.create_combinations = Mock(
            return_value=[
                {
                    "STS_home_team_win": 1.2,
                    "SUPERBET_away_team_win": 2.25,
                }
            ]
        )
        result = calculator.calculate_arbitrage()
        assert result == None


class Test_ThreeWayArbitrageCalculator:
    """
    Test Class:
    ------------
    This class contains unit tests for the ThreeWayArbitrageCalculator class.
    Each test method focuses on a specific functionality of the calculator.

    Fixtures:
    ---------
    - `event_mock`: A fixture providing a mocked Event object with standard
      events data for testing.
    - `positive_event_mock`: A fixture providing a mocked Event object with
      positive arbitrage opportunities for testing.
    - `expected_dataframe`: A fixture providing the expected result DataFrame.

    Notes:
    ------
    - The tests use mocked event objects to simulate event data.
    - Test data and specific values for calculations are provided in
        each method.
    - The results are checked against expected values to ensure accuracy.
    """
    @pytest.fixture
    def event_mock(self):
        events_data = {
            "STS": DataFrame(
                {
                    "event_name": "Karagumruk - Adana Demirspor",
                    "home_player": "KARAGUMRUKr",
                    "away_player": "ADANA DEMIRSPOR",
                    "event_date": "2023-10-23",
                    "home_team_win": 2.9,
                    "draw": 3.4,
                    "away_team_win": 2.22,
                },
                index=[0],
            ),
            "FORTUNA": DataFrame(
                {
                    "event_name": "Karagumruk - Adana Demirspor",
                    "home_player": "KARAGUMRUKr",
                    "away_player": "ADANA DEMIRSPOR",
                    "event_date": "2023-10-23",
                    "home_team_win": 2.9,
                    "draw": 3.55,
                    "away_team_win": 2.2,
                },
                index=[0],
            ),
            "BETCLIC": DataFrame(
                {
                    "event_name": "Karagumruk - Adana Demirspor",
                    "home_player": "KARAGUMRUKr",
                    "away_player": "ADANA DEMIRSPOR",
                    "event_date": "2023-10-23",
                    "home_team_win": 2.95,
                    "draw": 3.6,
                    "away_team_win": 2.22,
                },
                index=[0],
            ),
            "SUPERBET": DataFrame(
                {
                    "event_name": "Karagumruk - Adana Demirspor",
                    "home_player": "KARAGUMRUKr",
                    "away_player": "ADANA DEMIRSPOR",
                    "event_date": "2023-10-23",
                    "home_team_win": 3.0,
                    "draw": 3.7,
                    "away_team_win": 2.25,
                },
                index=[0],
            ),
        }
        mock_object = Mock(spec=Event)
        mock_object.events_data = events_data

        return mock_object

    @pytest.fixture
    def positive_event_mock(self):
        events_data = {
            "STS": DataFrame(
                {
                    "event_name": "Karagumruk - Adana Demirspor",
                    "home_player": "KARAGUMRUKr",
                    "away_player": "ADANA DEMIRSPOR",
                    "event_date": "2023-10-23",
                    "home_team_win": 3.5,
                    "draw": 3.4,
                    "away_team_win": 2.22,
                },
                index=[0],
            ),
            "FORTUNA": DataFrame(
                {
                    "event_name": "Karagumruk - Adana Demirspor",
                    "home_player": "KARAGUMRUKr",
                    "away_player": "ADANA DEMIRSPOR",
                    "event_date": "2023-10-23",
                    "home_team_win": 2.9,
                    "draw": 3.55,
                    "away_team_win": 2.2,
                },
                index=[0],
            ),
            "BETCLIC": DataFrame(
                {
                    "event_name": "Karagumruk - Adana Demirspor",
                    "home_player": "KARAGUMRUKr",
                    "away_player": "ADANA DEMIRSPOR",
                    "event_date": "2023-10-23",
                    "home_team_win": 2.95,
                    "draw": 4.4,
                    "away_team_win": 2.22,
                },
                index=[0],
            ),
            "SUPERBET": DataFrame(
                {
                    "event_name": "Karagumruk - Adana Demirspor",
                    "home_player": "KARAGUMRUKr",
                    "away_player": "ADANA DEMIRSPOR",
                    "event_date": "2023-10-23",
                    "home_team_win": 3.0,
                    "draw": 3.7,
                    "away_team_win": 4.5,
                },
                index=[0],
            ),
        }
        mock_object = Mock(spec=Event)
        mock_object.events_data = events_data

        return mock_object

    @pytest.fixture
    def expected_dataframe(self):
        return DataFrame(
            {
                "STS_index": 0,
                "STS_home_team_win": 2.9,
                "STS_draw": 3.4,
                "STS_away_team_win": 2.22,
                "FORTUNA_index": 0,
                "FORTUNA_home_team_win": 2.9,
                "FORTUNA_draw": 3.55,
                "FORTUNA_away_team_win": 2.2,
                "BETCLIC_index": 0,
                "BETCLIC_home_team_win": 2.95,
                "BETCLIC_draw": 3.6,
                "BETCLIC_away_team_win": 2.22,
                "SUPERBET_index": 0,
                "SUPERBET_home_team_win": 3.0,
                "SUPERBET_draw": 3.7,
                "SUPERBET_away_team_win": 2.25,
            },
            index=[0],
        )

    def test_create_data_source_return_dataframe(
        self, event_mock, expected_dataframe
    ):
        calculator = ThreeWayArbitrageCalculator(event_mock)
        result = calculator.create_data_source()
        assert result.equals(expected_dataframe)

    def test_create_combinations_return_right_number_of_combinations(
        self, event_mock
    ):
        calculator = ThreeWayArbitrageCalculator(event_mock)
        result = calculator.create_combinations()
        assert len(result) == 64

    def test_get_values_from_dict(self, event_mock):
        calculator = ThreeWayArbitrageCalculator(event_mock)
        dictionary = {
            "STS_home_team_win": 2.9,
            "FORTUNA_draw": 3.55,
            "BETCLIC_away_team_win": 2.22,
        }
        expected_return = (2.9, 3.55, 2.22)
        result = calculator.get_values_from_dict(dictionary)
        assert result == expected_return

    def test_calculate_implied_probability(self, event_mock):
        calculator = ThreeWayArbitrageCalculator(event_mock)
        result = calculator.calculate_implied_probability(
            home_odds=2.9, draw_odds=3.4, away_odds=2.22
        )
        assert round(result, 2) == 1.22

    def test_calculate_odds_value(self, event_mock):
        calculator = ThreeWayArbitrageCalculator(event_mock)
        result = calculator.calculate_odds_value(
            money_ratio=1.11, home_win=3.1, draw=4.4, away_win=3.6
        )
        home_odds = (
            Constant.TEST_STAKE * ((1 + Constant.TAX_VALUE) / 3.1) * 1.11
        )
        draw_odds = (
            Constant.TEST_STAKE * ((1 + Constant.TAX_VALUE) / 4.4) * 1.11
        )
        away_odds = (
            Constant.TEST_STAKE * ((1 + Constant.TAX_VALUE) / 3.6) * 1.11
        )
        assert result == (home_odds, draw_odds, away_odds)

    def test_calculate_final_return(self, event_mock):
        calculator = ThreeWayArbitrageCalculator(event_mock)
        home_win = 3.5
        home_money = 38.86
        draw_money = 30.91
        away_money = 30.23
        result = calculator.calculate_final_return(
            home_money, home_win, draw_money, away_money
        )
        assert round(result, 2) == 31.35

    def test_calculate_arbitrage_return_none_if_event_not_have_chanse(
        self, event_mock
    ):
        calculator = ThreeWayArbitrageCalculator(event_mock)
        result = calculator.calculate_arbitrage()
        assert result == None

    def test_calculate_arbitrage_return_dict_in_list_if_event_have_chanse(
        self, positive_event_mock
    ):
        calculator = ThreeWayArbitrageCalculator(positive_event_mock)
        result = calculator.calculate_arbitrage()
        for res in result:
            print(res)
        assert len(result) == 16

    def test_calculate_arbitrage_return_dict_if_event_have_chanse(
        self, positive_event_mock
    ):
        calculator = ThreeWayArbitrageCalculator(positive_event_mock)
        calculator.create_combinations = Mock(
            return_value=[
                {
                    "STS_home_team_win": 3.5,
                    "BETCLIC_draw": 4.4,
                    "SUPERBET_away_team_win": 4.5,
                }
            ]
        )
        result = calculator.calculate_arbitrage()
        assert result == [
            {
                "STS_home_team_win": 3.5,
                "BETCLIC_draw": 4.4,
                "SUPERBET_away_team_win": 4.5,
            }
        ]

    def test_calculate_arbitrage_return_dict_if_event_have_not_chanse(
        self, positive_event_mock
    ):
        calculator = ThreeWayArbitrageCalculator(positive_event_mock)
        calculator.create_combinations = Mock(
            return_value=[
                {
                    "STS_home_team_win": 2.9,
                    "BETCLIC_draw": 3.6,
                    "SUPERBET_away_team_win": 2.25,
                }
            ]
        )
        result = calculator.calculate_arbitrage()
        assert result == None
