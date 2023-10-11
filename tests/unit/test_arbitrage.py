import pytest
from unittest.mock import Mock
from utils.events import Event
from app.arbitrage import ArbitrageCalculator

class Test_ArbitrageCalculator:

    @pytest.fixture
    def event_mock(self):
        return Mock(spec=Event)

    def test_get_probability(self, event_mock):
        calculator = ArbitrageCalculator(event_mock)

        result = calculator.get_probability(1.2)
        assert result == 0.93

    def test_calculate_money_ratio(self, event_mock):
        calculator = ArbitrageCalculator(event_mock)
        event_probability = 0.90

        result = calculator.calculate_money_ratio(event_probability)
        assert result == 1.11

    def test_calculate_return(self, event_mock):
        calculator = ArbitrageCalculator(event_mock)
        money = 30.00
        odds = 1.20

        result = calculator.calculate_return(money=money, odds=odds)
        assert result == 36.00