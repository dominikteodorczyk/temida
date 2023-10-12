"""
Module Test_Arbitrage:

This module contains unit tests for the classes and methods defined in the
arbitrage module. The tests cover various functionalities related to arbitrage
calculations for different types of events and outcomes.

Classes:
--------
1. Test_TwoWayArbitrageCalculator: Unit tests for the ArbitrageCalculator
    class.
2. Test_TwoWayArbitrageCalculator: Unit tests for the
    TwoWayArbitrageCalculator class.
3. Test_ThreeWayArbitrageCalculator: Unit tests for the
    ThreeWayArbitrageCalculator class.

Test Cases:
-----------
The test cases cover various scenarios, including calculating implied
probabilities, creating combinations, and checking for arbitrage opportunities.
The fixtures provide predefined event data for testing.

Usage:
------
To run the tests, use a testing framework such as pytest with the following
command: pytest test_arbitrage.py
"""

from unittest.mock import Mock
import pytest
from pandas import DataFrame
from utils.events import Event
from utils.technical import Constant
from app.arbitrage import (
    ArbitrageCalculator,
    TwoWayArbitrageCalculator,
    ThreeWayArbitrageCalculator,
)


class Test_ArbitrageCalculator:
    """
    Test Class:
    ------------
    This class contains unit tests for the ArbitrageCalculator class
    methods. Each test method focuses on a specific functionality of
    the calculator.

    Notes:
    ------
    - The tests use a mocked event object to simulate event data.
    - Test data and specific values for calculations are provided in
        each method.
    - The results are checked against expected values to ensure accuracy.
    """

    @pytest.fixture
    def event_mock(self):
        return Mock(spec=Event)

    def test_get_probability(self, event_mock):
        """
        Test Case:
        ----------
        The method calculates the implied probability using the provided
        odds and verifies that the result is within an acceptable range
        of the expected probability.

        Steps:
        ------
        1. Create an ArbitrageCalculator instance with the mocked event.
        2. Call the get_probability method with a specified odds value (1.2).
        3. Check that the result, when rounded to two decimal places, matches
            the expected implied probability (0.93).
        """
        calculator = ArbitrageCalculator(event_mock)
        result = calculator.get_probability(1.2)
        assert round(result, 2) == 0.93

    def test_calculate_money_ratio(self, event_mock):
        """
        Test Case:
        ----------
        The method calculates the money ratio based on a given event
        probability  and ensures that the result is within an acceptable
        range.

        Steps:
        ------
        1. Create an ArbitrageCalculator instance with the mocked event.
        2. Set a specific event probability (0.90).
        3. Call the calculate_money_ratio method with the provided
            probability.
        4. Check that the result, when rounded to two decimal places, m
            atches the expected money ratio (1.11).
        """
        calculator = ArbitrageCalculator(event_mock)
        event_probability = 0.90
        result = calculator.calculate_money_ratio(event_probability)
        assert round(result, 2) == 1.11

    def test_calculate_return(self, event_mock):
        """
        Test Case:
        ----------
        The method calculates the potential return based on the provided
        stake amount and odds and ensures that the result is within
        an acceptable range.

        Steps:
        ------
        1. Create an ArbitrageCalculator instance with the mocked event.
        2. Set specific values for the stake amount (100.00) and odds (1.20).
        3. Call the calculate_return method with the provided money and odds.
        4. Check that the result, when rounded to two decimal places, matches
            the expected return (120.00).
        """
        calculator = ArbitrageCalculator(event_mock)
        money = 100.00
        odds = 1.20
        result = calculator.calculate_return(money=money, odds=odds)
        assert round(result, 2) == 120.00


class Test_TwoWayArbitrageCalculator:
    """
    Test Class:
    ------------
    This class contains unit tests for the TwoWayArbitrageCalculator class.
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
        """
        Test Case:
        ----------
        The method tests the create_data_source method of the
        TwoWayArbitrageCalculator class to ensure it returns
        the expected DataFrame.

        1. Create an instance of TwoWayArbitrageCalculator with
            the positive_event_mock_two_way fixture.
        2. Call the create_data_source method.
        3. Check if the result DataFrame is equal to the
            expected_dataframe fixture.
        """
        calculator = TwoWayArbitrageCalculator(positive_event_mock_two_way)
        result = calculator.create_data_source()
        assert result.equals(expected_dataframe)

    def test_create_combinations_return_right_number_of_combinations(
        self, positive_event_mock_two_way
    ):
        """
        Test Case:
        ----------
        The method tests the create_combinations method of the
        TwoWayArbitrageCalculator class to ensure it returns the correct
        number of combinations.

        1. Create an instance of TwoWayArbitrageCalculator with the
            positive_event_mock_two_way fixture.
        2. Call the create_combinations method.
        3. Check if the length of the result list is equal to the
            expected number of combinations (16).
        """
        calculator = TwoWayArbitrageCalculator(positive_event_mock_two_way)
        result = calculator.create_combinations()
        assert len(result) == 16

    def test_get_values_from_dict(self, event_mock):
        """
        Test Case:
        ----------
        The method tests the get_values_from_dict method of the
        TwoWayArbitrageCalculator class to ensure it extracts the correct
        values from the provided dictionary.

        1. Create an instance of TwoWayArbitrageCalculator with the
            event_mock fixture.
        2. Define a dictionary with specific keys representing odds
            from different sources.
        3. Call the get_values_from_dict method with the dictionary.
        4. Check if the returned values match the expected values.

        Notes:
        ------
        The test verifies that the get_values_from_dict method correctly
        extracts the odds corresponding to the "home_team_win" and
        "away_team_win" keys from the given dictionary.
        """
        calculator = TwoWayArbitrageCalculator(event_mock)
        dictionary = {
            "STS_home_team_win": 2.9,
            "BETCLIC_away_team_win": 2.22,
        }
        expected_return = (2.9, 2.22)
        result = calculator.get_values_from_dict(dictionary)
        assert result == expected_return

    def test_calculate_implied_probability(self, event_mock):
        """
        Test Case:
        ----------
        The method tests the calculate_implied_probability method of the
        TwoWayArbitrageCalculator class to ensure it calculates the implied
        probability correctly.

        1. Create an instance of TwoWayArbitrageCalculator with the
            event_mock fixture.
        2. Call the calculate_implied_probability method with specific
            home and away odds.
        3. Check if the calculated implied probability, rounded to two
            decimal places, matches the expected value.

        Notes:
        ------
        The test verifies that the calculate_implied_probability method
        correctly calculates the implied probability based on the provided
        home and away odds.
        """
        calculator = TwoWayArbitrageCalculator(event_mock)
        result = calculator.calculate_implied_probability(
            home_odds=2.9, away_odds=2.22
        )
        assert round(result, 2) == 0.89

    def test_calculate_odds_value(self, event_mock):
        """
        Test Case:
        ----------
        The method tests the calculate_odds_value method of the
        TwoWayArbitrageCalculator class to ensure it correctly calculates
        the adjusted odds values.

        1. Create an instance of TwoWayArbitrageCalculator with the
            event_mock fixture.
        2. Call the calculate_odds_value method with specified parameters.
        3. Check if the method correctly calculates the adjusted home
            and away odds values based on the provided money ratio.

        Constants:
        ----------
        - `Constant.TEST_STAKE`: A constant representing the test stake amount.
        - `Constant.TAX_VALUE`: A constant representing the tax value.

        Notes:
        ------
        The test verifies that the calculate_odds_value method correctly
        calculates the adjusted home and away odds values based on the provided
        parameters.
        """
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
        """
        Test Case:
        ----------
        The method tests the calculate_final_return method of the
        TwoWayArbitrageCalculator class to ensure it correctly calculates
        the final return for a given outcome.

        1. Create an instance of TwoWayArbitrageCalculator with the
            event_mock fixture.
        2. Specify values for home win odds, home money, and away money.
        3. Call the calculate_final_return method with the specified
            parameters.
        4. Check if the method correctly calculates the final return
            for the provided outcome.

        Constants:
        ----------
        - `Constant.TAX_VALUE`: A constant representing the tax value.

        Notes:
        ------
        The test verifies that the calculate_final_return method correctly
        calculates the final return for a given outcome based on the provided
        odds and money values.
        """
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
        """
        Test Case:
        ----------
        The method tests the calculate_arbitrage method of the
        TwoWayArbitrageCalculator class to ensure it returns None when
        the event does not have a chance of occurring.

        1. Create an instance of TwoWayArbitrageCalculator with the
            event_mock fixture.
        2. Call the calculate_arbitrage method.
        3. Check if the method returns None when the event does not
            have a chance.

        Notes:
        ------
        The test verifies that the calculate_arbitrage method returns
        None when the implied probability of the event is less than 1.00,
        indicating no chance.
        """
        calculator = TwoWayArbitrageCalculator(event_mock)
        result = calculator.calculate_arbitrage()
        assert result is None

    def test_calculate_arbitrage_return_dict_in_list_if_event_have_chanse(
        self, positive_event_mock_two_way
    ):
        """
        Test Case:
        ----------
        The method tests the calculate_arbitrage method of the
        TwoWayArbitrageCalculator class to ensure it returns a list of
        dictionaries when the event has a chance of occurring.

        1. Create an instance of TwoWayArbitrageCalculator with the
            positive_event_mock_two_way fixture.
        2. Call the calculate_arbitrage method.
        3. Check if the method returns a list of dictionaries when the
            event has a chance.

        Notes:
        ------
        The test verifies that the calculate_arbitrage method returns a
        list of dictionaries when the implied probability of the event is
        less than 1.00, indicating a chance. The length of the list should be
        equal to the number of combinations of two-way arbitrage.
        """
        calculator = TwoWayArbitrageCalculator(positive_event_mock_two_way)
        result = calculator.calculate_arbitrage()
        assert len(result) == 16

    def test_calculate_arbitrage_return_dict_if_event_have_chanse(
        self, positive_event_mock_two_way
    ):
        """
        Test Case:
        ----------
        The method tests the calculate_arbitrage method of the
        TwoWayArbitrageCalculator class to ensure it returns a list of
        dictionaries when the event has a chance of occurring.

        1. Create an instance of TwoWayArbitrageCalculator with the
            positive_event_mock_two_way fixture.
        2. Mock the create_combinations method to return a specific list
            of dictionaries.
        3. Call the calculate_arbitrage method.
        4. Check if the method returns the expected list of dictionaries
            when the event has a chance.

        Notes:
        ------
        The test verifies that the calculate_arbitrage method returns a
        list of dictionaries when the implied probability of the event is
        less than 1.00, indicating a chance. The method should use the mocked
        create_combinations method, and the result should match the expected
        list of dictionaries.
        """
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
        """
        Test Case:
        ----------
        The method tests the calculate_arbitrage method of the
        TwoWayArbitrageCalculator class to ensure it returns None when the
        event does not have a chance of occurring.

        1. Create an instance of TwoWayArbitrageCalculator with the
            positive_event_mock_two_way fixture.
        2. Mock the create_combinations method to return a specific list
            of dictionaries.
        3. Call the calculate_arbitrage method.
        4. Check if the method returns None when the implied probability of
            the event is greater than or equal to 1.00.

        Notes:
        ------
        The test verifies that the calculate_arbitrage method returns
        None when the implied probability of the event is greater than or
        equal to 1.00, indicating no chance of occurrence. The method should
        use the mocked create_combinations method, and the result should
        be None.
        """
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
        assert result is None


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
        """
        Test Case:
        ----------
        The method tests the create_data_source method of the
        ThreeWayArbitrageCalculator class to ensure it returns
        the expected DataFrame.

        1. Create an instance of ThreeWayArbitrageCalculator with
            the event_mock fixture.
        2. Call the create_data_source method.
        3. Check if the result DataFrame is equal to the
            expected_dataframe fixture.
        """
        calculator = ThreeWayArbitrageCalculator(event_mock)
        result = calculator.create_data_source()
        assert result.equals(expected_dataframe)

    def test_create_combinations_return_right_number_of_combinations(
        self, event_mock
    ):
        """
        Test Case:
        ----------
        The method tests the create_combinations method of the
        ThreeWayArbitrageCalculator class to ensure it returns the correct
        number of combinations.

        1. Create an instance of ThreeWayArbitrageCalculator with the
            event_mock fixture.
        2. Call the create_combinations method.
        3. Check if the length of the result list is equal to the
            expected number of combinations (64).
        """
        calculator = ThreeWayArbitrageCalculator(event_mock)
        result = calculator.create_combinations()
        assert len(result) == 64

    def test_get_values_from_dict(self, event_mock):
        """
        Test Case:
        ----------
        The method tests the get_values_from_dict method of the
        ThreeWayArbitrageCalculator class to ensure it extracts the correct
        values from the provided dictionary.

        1. Create an instance of ThreeWayArbitrageCalculator with the
            event_mock fixture.
        2. Define a dictionary with specific keys representing odds
            from different sources.
        3. Call the get_values_from_dict method with the dictionary.
        4. Check if the returned values match the expected values.

        Notes:
        ------
        The test verifies that the get_values_from_dict method correctly
        extracts the odds corresponding to the "home_team_win", "draw" and
        "away_team_win" keys from the given dictionary.
        """
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
        """
        Test Case:
        ----------
        The method tests the calculate_implied_probability method of the
        ThreeWayArbitrageCalculator class to ensure it calculates the implied
        probability correctly.

        1. Create an instance of ThreeWayArbitrageCalculator with the
            event_mock fixture.
        2. Call the calculate_implied_probability method with specific
            home, draw and away odds.
        3. Check if the calculated implied probability, rounded to two
            decimal places, matches the expected value.

        Notes:
        ------
        The test verifies that the calculate_implied_probability method
        correctly calculates the implied probability based on the provided
        home, draw and away odds.
        """
        calculator = ThreeWayArbitrageCalculator(event_mock)
        result = calculator.calculate_implied_probability(
            home_odds=2.9, draw_odds=3.4, away_odds=2.22
        )
        assert round(result, 2) == 1.22

    def test_calculate_odds_value(self, event_mock):
        """
        Test Case:
        ----------
        The method tests the calculate_odds_value method of the
        ThreeWayArbitrageCalculator class to ensure it correctly calculates
        the adjusted odds values.

        1. Create an instance of ThreeWayArbitrageCalculator with the
            event_mock fixture.
        2. Call the calculate_odds_value method with specified parameters.
        3. Check if the method correctly calculates the adjusted home, draw
            and away odds values based on the provided money ratio.

        Constants:
        ----------
        - `Constant.TEST_STAKE`: A constant representing the test stake amount.
        - `Constant.TAX_VALUE`: A constant representing the tax value.

        Notes:
        ------
        The test verifies that the calculate_odds_value method correctly
        calculates the adjusted home, draw and away odds values based on
        the provided parameters.
        """
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
        """
        Test Case:
        ----------
        The method tests the calculate_final_return method of the
        ThreeWayArbitrageCalculator class to ensure it correctly calculates
        the final return for a given outcome.

        1. Create an instance of ThreeWayArbitrageCalculator with the
            event_mock fixture.
        2. Specify values for home win odds, home money, draw_money and
            away money.
        3. Call the calculate_final_return method with the specified
            parameters.
        4. Check if the method correctly calculates the final return
            for the provided outcome.

        Constants:
        ----------
        - `Constant.TAX_VALUE`: A constant representing the tax value.

        Notes:
        ------
        The test verifies that the calculate_final_return method correctly
        calculates the final return for a given outcome based on the provided
        odds and money values.
        """
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
        """
        Test Case:
        ----------
        The method tests the calculate_arbitrage method of the
        ThreeWayArbitrageCalculator class to ensure it returns None when
        the event does not have a chance of occurring.

        1. Create an instance of ThreeWayArbitrageCalculator with the
            event_mock fixture.
        2. Call the calculate_arbitrage method.
        3. Check if the method returns None when the implied probability
            of the event is greater than or equal to 1.00.

        Notes:
        ------
        The test verifies that the calculate_arbitrage method returns
        None when the implied probability of the event is greater than or
        equal to 1.00, indicating no chance of occurrence. The method should
        use the mocked event data, and the result should be None.
        """
        calculator = ThreeWayArbitrageCalculator(event_mock)
        result = calculator.calculate_arbitrage()
        assert result is None

    def test_calculate_arbitrage_return_dict_in_list_if_event_have_chanse(
        self, positive_event_mock
    ):
        """
        Test Case:
        ----------
        The method tests the calculate_arbitrage method of the
        ThreeWayArbitrageCalculator class to ensure it returns a list of
        dictionaries when the event has a chance of occurring.

        1. Create an instance of ThreeWayArbitrageCalculator with
            the positive_event_mock fixture.
        2. Call the calculate_arbitrage method.
        3. Iterate through each dictionary in the result (if not None)
            and print it.
        4. Check if the length of the result list is 16.

        Notes:
        ------
        The test verifies that the calculate_arbitrage method returns
        a list of dictionaries, each representing a combination of odds
        for home team win, draw, and away team win. The length of the result
        list should be 16, as there are 16 possible combinations.
        """
        calculator = ThreeWayArbitrageCalculator(positive_event_mock)
        result = calculator.calculate_arbitrage()
        for res in result:
            print(res)
        assert len(result) == 16

    def test_calculate_arbitrage_return_dict_if_event_have_chanse(
        self, positive_event_mock
    ):
        """
        Test Case:
        ----------
        The method tests the calculate_arbitrage method of the
        ThreeWayArbitrageCalculator class to ensure it returns a list
        containing a dictionary when the event has a chance of occurring.

        1. Create an instance of ThreeWayArbitrageCalculator with the
            positive_event_mock fixture.
        2. Mock the create_combinations method to return a list with
            a specific combination dictionary.
        3. Call the calculate_arbitrage method.
        4. Check if the result is a list containing the expected
            combination dictionary.

        Notes:
        ------
        The test verifies that the calculate_arbitrage method returns
        a list containing a dictionary, representing a combination of odds
        for home team win, draw, and away team win. The method uses a mocked
        create_combinations method to control the returned combinations.
        """
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
        """
        Test Case:
        ----------
        The method tests the calculate_arbitrage method of the
        ThreeWayArbitrageCalculator  class to ensure it returns None
        when the event has no chance of occurring.

        1. Create an instance of ThreeWayArbitrageCalculator with the
            positive_event_mock fixture.
        2. Mock the create_combinations method to return a list with
            a specific combination dictionary.
        3. Call the calculate_arbitrage method.
        4. Check if the result is None.

        Notes:
        ------
        The test verifies that the calculate_arbitrage method returns
        None when the event has no chance of a profitable combination.
        The method uses a mocked create_combinations method to control
        the returned combinations.
        """
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
        assert result is None
