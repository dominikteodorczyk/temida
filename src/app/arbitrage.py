from utils.events import *
from pandas import concat
from typing import Union
from utils.technical import Constant


class Arbitrage:
    # TODO: clasa wykonująca arbitraż na całej tablicy
    def __init__(self, data_object: MainEventsBoard) -> None:
        self.data_object = data_object
        self_arbitrage_pair = DataFrame()

    def calculate_arbitage(self):
        for index, row in self.data_object.events_table.iterrows():
            event = Event.create(row, self.data_object.events_dict)
            print("-------------")
            print(event.events_data)
            arbitrage = EventArbitrage.create(event)
            # arbitrage.parepare_data()


class EventArbitrage:
    def __init__(self, event_object, event_name, event_date, calc) -> None:
        self.event_data: Event = event_object
        self.event_name = event_name
        self.event_date = event_date
        self.calculator = calc

    def __str__(self) -> str:
        return self.event_name

    @classmethod
    def create(cls, event_object: Event):
        first_key = event_object.events_data[
            list(event_object.events_data.keys())[0]
        ]
        event_name = first_key["event_name"].iloc[0]
        event_date = first_key["event_date"].iloc[0]
        if first_key.shape[1] == 8:
            return cls(
                event_object,
                event_name,
                event_date,
                ThreeWayArbitrageCalculator(event_object),
            )
        elif first_key == 7:
            return cls(
                event_object,
                event_name,
                event_date,
                TwoWayArbitrageCalculator(event_object),
            )

    def parepare_data(self):
        # bets_dataframe = self.calculator.create_data_source(self.event_data)
        # bets_combination = self.calculator.create_combinations(bets_dataframe)
        # print(bets_combination)
        pass


class ArbitrageCalculator:
    def __init__(self, event_data) -> None:
        self.event_data = event_data

    def get_probability(self, odds: float) -> float:
        """
        Calculates the probability of an event based on the odds.

        Parameters:
        --------
        - odds (float): The odds of the bet.

        Returns:
        --------
        float: The calculated probability.
        """
        return (1 + Constant.TAX_VALUE) / odds

    def calculate_money_ratio(self, event_probability: float) -> float:
        """
        Calculates the ratio of the amount of money placed to the
        probability of the event.

        Parameters:
        --------
        - event_probability (float): The probability of the event.

        Returns:
        --------
        float: The calculated money ratio.
        """
        return (100 / event_probability) / 100

    def calculate_return(self, money: float, odds: float) -> float:
        """
        Calculates the potential return based on the amount of money
        placed and the odds.

        Parameters:
        --------
        - money (float): The amount of money placed.
        - odds (float): The odds of the bet.

        Returns:
        --------
        float: The calculated potential return.
        """
        return money * odds


class TwoWayArbitrageCalculator(ArbitrageCalculator):
    def __init__(self, event_data) -> None:
        super().__init__(event_data)

    def create_data_source(self) -> DataFrame:
        """
        Creates a consolidated DataFrame from event-specific data.

        Returns:
        --------
        pandas.DataFrame: The consolidated DataFrame.
        """
        dataframes_dict = {}
        for key, value in self.event_data.events_data.items():
            dataframes_dict[key] = (
                value[["home_team_win", "away_team_win"]]
                .reset_index()
                .add_prefix(f"{key}_")
            )

        result_df = concat(dataframes_dict.values(), axis=1)
        return result_df.reset_index(drop=True)

    def create_combinations(self) -> list:
        """
        Creates combinations of bets from the DataFrame.

        Returns:
        --------
        list: A list of dictionaries representing all bet combinations.
        """
        bets_dataframe = self.create_data_source()
        all_columns = (bets_dataframe.columns).to_list()
        home_win_cols = [s for s in all_columns if s.endswith("home_team_win")]
        away_win_cols = [s for s in all_columns if s.endswith("away_team_win")]

        list_of_dicts = []
        for home_col in home_win_cols:
            for away_col in away_win_cols:
                dictionary = {
                    home_col: bets_dataframe[home_col].iloc[0],
                    away_col: bets_dataframe[away_col].iloc[0],
                }
                list_of_dicts.append(dictionary)

        return list_of_dicts

    def get_values_from_dict(self, dictionary):
        """
        Extract home win and away win values from a dictionary.

        Parameters:
        --------
        - dictionary (dict): A dictionary containing keys related
            to match outcomes.

        Returns:
        --------
        tuple: A tuple containing home win and away win values.
        """
        home_win_key = [
            key for key in dictionary.keys() if key.endswith("home_team_win")
        ][0]
        away_win_key = [
            key for key in dictionary.keys() if key.endswith("away_team_win")
        ][0]

        home_win = dictionary[home_win_key]
        away_win = dictionary[away_win_key]

        return home_win, away_win

    def calculate_implied_probability(
        self, home_odds: float, away_odds: float
    ) -> float:
        """
        Calculate the total implied probability based on home and win
        probabilities.

        Parameters:
        --------
        - home_odds (float): The odds of home team winning.
        - away_odds (float): The odds of the away team winning.

        Returns:
        --------
        float: The total implied probability.
        """
        return (
            self.get_probability(home_odds)
            + self.get_probability(away_odds)
        )

    def calculate_odds_value(
        self, money_ratio: float, home_win: float, away_win: float
    ):
        """
        Calculates the values of bets for test outcomes.

        Parameters:
        --------
        - money_ratio (float): The ratio indicating the amount of
            money placed.
        - home_win (float): odds for a bet on the home team winning.
        - away_win (float): odds for a bet on the away team winning.

        Returns:
        --------
        tuple: A tuple containing the calculated values for bets on
        home team win and away team win.
        """
        return (
            Constant.TEST_STAKE * self.get_probability(home_win) * money_ratio,
            Constant.TEST_STAKE * self.get_probability(away_win) * money_ratio,
        )

    def calculate_final_return(
        self, win_return, win_odds, *deductions
    ) -> float:
        """
        Calculate the final return after deducting various costs.

        Parameters:
        --------
        - win_return (float): The return from a successful event.
        - *deductions (float): Debt from unsuccessful events.

        Returns:
        --------
        float: The final return after deducting all costs.
        """
        return (win_return * (win_odds - (1 + Constant.TAX_VALUE))) - sum(
            deductions
        )

    def calculate_arbitrage(self):
        """
        Calculate arbitrage opportunities based on the given event data.

        This method calculates the implied probability of outcomes
        (home win and away win), checks for arbitrage opportunities,
        and prints the event data if profitable opportunities are found.

        Returns:
        --------
        list or None: Returns the list of bets data if arbitrage opportunities
        are found, otherwise returns None.

        Notes:
        ------
        The arbitrage opportunities are checked based on the calculated
        implied probabilities, money ratios, and final returns for each
        possible outcome.
        """
        combinations = self.create_combinations()
        possible_positiv_return_combination = []
        for combination in combinations:
            home_win, away_win = self.get_values_from_dict(combination)
            event_probability = self.calculate_implied_probability(
                home_win, away_win
            )

            if event_probability >= 1.00:
                pass
            else:
                money_ratio = self.calculate_money_ratio(event_probability)
                home_money, away_money = self.calculate_odds_value(
                    money_ratio, home_win, away_win
                )
                if all(
                    x > Constant.TOTAL_MIN_RETURN
                    for x in [
                        self.calculate_final_return(
                            home_money, home_win,  away_money
                        ),
                        self.calculate_final_return(
                            away_money, away_win, home_money
                        ),
                    ]
                ):
                    possible_positiv_return_combination.append(combination)
                else:
                    pass
        if possible_positiv_return_combination:
            return possible_positiv_return_combination
        else:
            return None


class ThreeWayArbitrageCalculator(ArbitrageCalculator):
    def __init__(self, event_data) -> None:
        super().__init__(event_data)

    def create_data_source(self) -> DataFrame:
        """
        Creates a consolidated DataFrame from event-specific data.

        Returns:
        --------
        pandas.DataFrame: The consolidated DataFrame.
        """
        dataframes_dict = {}
        for key, value in self.event_data.events_data.items():
            dataframes_dict[key] = (
                value[["home_team_win", "draw", "away_team_win"]]
                .reset_index()
                .add_prefix(f"{key}_")
            )

        result_df = concat(dataframes_dict.values(), axis=1)
        return result_df.reset_index(drop=True)

    def create_combinations(self) -> list:
        """
        Creates combinations of bets from the DataFrame.

        Returns:
        --------
        list: A list of dictionaries representing all bet combinations.
        """
        bets_dataframe = self.create_data_source()
        all_columns = (bets_dataframe.columns).to_list()
        home_win_cols = [s for s in all_columns if s.endswith("home_team_win")]
        draw_cols = [s for s in all_columns if s.endswith("draw")]
        away_win_cols = [s for s in all_columns if s.endswith("away_team_win")]

        list_of_dicts = []
        for home_col in home_win_cols:
            for draw_col in draw_cols:
                for away_col in away_win_cols:
                    dictionary = {
                        home_col: bets_dataframe[home_col].iloc[0],
                        draw_col: bets_dataframe[draw_col].iloc[0],
                        away_col: bets_dataframe[away_col].iloc[0],
                    }
                    list_of_dicts.append(dictionary)

        return list_of_dicts

    def get_values_from_dict(self, dictionary):
        """
        Extract home win, draw, and away win values from a dictionary.

        Parameters:
        --------
        - dictionary (dict): A dictionary containing keys related
            to match outcomes.

        Returns:
        --------
        tuple: A tuple containing home win, draw, and away win values.
        """
        home_win_key = [
            key for key in dictionary.keys() if key.endswith("home_team_win")
        ][0]
        draw_key = [key for key in dictionary.keys() if key.endswith("draw")][
            0
        ]
        away_win_key = [
            key for key in dictionary.keys() if key.endswith("away_team_win")
        ][0]

        home_win = dictionary[home_win_key]
        draw = dictionary[draw_key]
        away_win = dictionary[away_win_key]

        return home_win, draw, away_win

    def calculate_implied_probability(
        self, home_odds: float, draw_odds: float, away_odds: float
    ) -> float:
        """
        Calculate the total implied probability based on home, draw,
        and win probabilities.

        Parameters:
        --------
        - home_odds (float): The odds of home team winning.
        - draw_odds (float): The odds of the match ending in a draw.
        - away_odds (float): The odds of the away team winning.

        Returns:
        --------
        float: The total implied probability.
        """
        return (
            self.get_probability(home_odds)
            + self.get_probability(draw_odds)
            + self.get_probability(away_odds)
        )

    def calculate_odds_value(
        self, money_ratio: float, home_win: float, draw: float, away_win: float
    ):
        """
        Calculates the values of bets for test outcomes.

        Parameters:
        --------
        - money_ratio (float): The ratio indicating the amount of
            money placed.
        - home_win (float): odds for a bet on the home team winning.
        - draw (float): odds for a bet on a draw.
        - away_win (float): odds for a bet on the away team winning.

        Returns:
        --------
        tuple: A tuple containing the calculated values for bets on
        home team win, draw, and away team win.
        """
        return (
            Constant.TEST_STAKE * self.get_probability(home_win) * money_ratio,
            Constant.TEST_STAKE * self.get_probability(draw) * money_ratio,
            Constant.TEST_STAKE * self.get_probability(away_win) * money_ratio,
        )

    def calculate_final_return(
        self, win_return, win_odds, *deductions
    ) -> float:
        """
        Calculate the final return after deducting various costs.

        Parameters:
        --------
        - win_return (float): The return from a successful event.
        - *deductions (float): Debt from unsuccessful events.

        Returns:
        --------
        float: The final return after deducting all costs.
        """
        return (win_return * (win_odds - (1 + Constant.TAX_VALUE))) - sum(
            deductions
        )

    def calculate_arbitrage(self):
        """
        Calculate arbitrage opportunities based on the given event data.

        This method calculates the implied probability of outcomes
        (home win, draw, away win), checks for arbitrage opportunities,
        and prints the event data if profitable opportunities are found.

        Returns:
        --------
        list or None: Returns the list of bets data if arbitrage opportunities
        are found, otherwise returns None.

        Notes:
        ------
        The arbitrage opportunities are checked based on the calculated
        implied probabilities, money ratios, and final returns for each
        possible outcome.
        """
        combinations = self.create_combinations()
        possible_positiv_return_combination = []
        option = None
        for combination in combinations:
            home_win, draw, away_win = self.get_values_from_dict(combination)
            event_probability = self.calculate_implied_probability(
                home_win, draw, away_win
            )

            if event_probability >= 1.00:
                pass
            else:
                money_ratio = self.calculate_money_ratio(event_probability)
                home_money, draw_money, away_money = self.calculate_odds_value(
                    money_ratio, home_win, draw, away_win
                )
                if all(
                    x > Constant.TOTAL_MIN_RETURN
                    for x in [
                        self.calculate_final_return(
                            home_money, home_win, draw_money, away_money
                        ),
                        self.calculate_final_return(
                            draw_money, draw, home_money, away_money
                        ),
                        self.calculate_final_return(
                            away_money, away_win, home_money, draw_money
                        ),
                    ]
                ):
                    possible_positiv_return_combination.append(combination)
                else:
                    pass
        if possible_positiv_return_combination:
            return possible_positiv_return_combination
        else:
            return None
