"""
App module contains classes for sports betting data collection, analysis,
and email notifications.

This module comprises classes that work together to collect sports
betting data, analyze the market, and handle email notifications for
potential bets.

Classes:
--------
1. MainOperator: Class for initializing the application and printing results.
2. DisciplineOperator: Class for scanning the sports betting market and
    identifying opportunities.
3. MailOperator: Class for managing the sending of emails for potential bets.

Usage:
------
The classes in this module can be used to build a streamlined sports
betting analysis and notification system. The workflow typically involves
initializing the necessary operators, scanning the market, and handling
email notifications.
"""

from pandas import DataFrame
from application.webscrper import ScrapersPool
from application.arbitrage import Arbitrage
from utils.sports import EventsTypes
from utils.technical import setup_logger


class MainOperator:
    """
    MainOperator class initializes the application and prints the results.
    This class serves as the main entry point for the application. It
    creates an instance of the DataOperator class to retrieve sports betting
    data, prints the results, and facilitates further processing.
    """

    def __init__(self) -> None:
        self.reuslts = DataOperator()
        self.reuslts.get_data()
        self.reuslts.sort_data()
        self.logging = setup_logger(name="MAIN_OPERATOR", print_logs=True)

        if not self.reuslts.two_way_results.empty:
            self.logging.info(
                "Two ways bets:\n%s", self.reuslts.two_way_results.to_string()
            )
        if not self.reuslts.three_way_results.empty:
            self.logging.info(
                "Three ways bets:\n%s",
                self.reuslts.three_way_results.to_string(),
            )


class DataOperator:
    """
    DataOperator class manages the retrieval of sports betting data.

    This class contains a static method, get_data(), that iterates over
    different sports and bet types, retrieves data using DisciplineOperator,
    and prints the opportunities.

    Attributes:
    - results (list): A list to store results retrieved for different sports s
        and bet types.
    - two_way_results (DataFrame): A DataFrame to store results for two-way
        betting opportunities.
    - three_way_results (DataFrame): A DataFrame to store results for
        three-way betting opportunities.
    """

    def __init__(self) -> None:
        self.results = []
        self.two_way_results = DataFrame()
        self.three_way_results = DataFrame()
        self.logging = setup_logger(name="DATA_OPERATOR", print_logs=True)

    def get_data(self):
        """
        Retrieves sports betting data for various sports and bet types.
        """
        for sport, bet_type in EventsTypes().sports.items():
            try:
                self.results.append(
                    DisciplineOperator(sport, bet_type).scan_market()
                )
                self.logging.info(f"{sport} data scraped")
            except:
                self.logging.warning(f"{sport} data not scraped")
        self.logging.info("Data scraping is finished")

    def get_odds_value_with_bookmaker(self, opp: dict, ends_with: str):
        odds_key: str = [key for key in opp.keys() if key.endswith(ends_with)][
            0
        ]
        bet_value: float = opp[odds_key]
        bookmaker: str = odds_key.replace(f"_{ends_with}", "")
        return f"{bet_value} ({bookmaker})"

    def sort_two_way(
        self,
        opportunity: list,
        sport: str,
        event_data: tuple,
        names_variation: list,
    ):
        """
        Sorts and stores data for two-way betting opportunities.

        Args:
        - opportunity (list): List of betting opportunities for a specific
            event.
        - sport (str): The sport for which the data is sorted.
        - event_data (tuple): Tuple containing event details (name, date).
        - names_variation (list): List of name variations for the event
            participants.
        """
        for opp in opportunity:
            i = 1
            event_to_table = {
                "sport": sport,
                "event": event_data[0],
                "event date": event_data[1],
                "1": self.get_odds_value_with_bookmaker(opp, "home_team_win"),
                "2": self.get_odds_value_with_bookmaker(opp, "away_team_win"),
            }
            for name_variation in names_variation:
                event_to_table[f"name_{i}"] = name_variation
                i += 1

            self.two_way_results = self.two_way_results._append(
                event_to_table, ignore_index=True
            )

    def sort_three_way(
        self,
        opportunity: list,
        sport: str,
        event_data: tuple,
        names_variation: list,
    ):
        """
        Sorts and stores data for three-way betting opportunities.

        Args:
        - opportunity (list): List of betting opportunities for a specific
            event.
        - sport (str): The sport for which the data is sorted.
        - event_data (tuple): Tuple containing event details (name, date).
        - names_variation (list): List of name variations for the event
            participants.
        """
        for opp in opportunity:
            i = 1
            event_to_table = {
                "sport": sport,
                "event": event_data[0],
                "event date": event_data[1],
                "1": self.get_odds_value_with_bookmaker(opp, "home_team_win"),
                "X": self.get_odds_value_with_bookmaker(opp, "draw"),
                "2": self.get_odds_value_with_bookmaker(opp, "away_team_win"),
            }
            for name_variation in names_variation:
                event_to_table[f"name_{i}"] = name_variation
                i += 1

            self.three_way_results = self.three_way_results._append(
                event_to_table, ignore_index=True
            )

    def sort_data(self):
        """
        Sorts and stores data for both two-way and three-way betting
        opportunities.
        """
        for sport_type in self.results:
            sport = next(iter(sport_type.keys()))
            for event in sport_type[sport]:
                if event:
                    event_data = next(iter(event.keys()))
                    event_values = next(iter(event.values()))
                    names_variation = event_values[0]
                    opportunity = event_values[1]
                    if len(opportunity[0]) == 3:
                        self.sort_three_way(
                            opportunity, sport, event_data, names_variation
                        )
                    if len(opportunity[0]) == 2:
                        self.sort_two_way(
                            opportunity, sport, event_data, names_variation
                        )


class DisciplineOperator:
    """
    This class takes a specific sport and bet type, initializes a ScrapersPool
    to fetch data, creates an events table, calculates arbitrage opportunities,
    and returns the results.

    Attributes:
    -----------
    sport (str): The specific sport to scan.
    bet_type (int): The type of sports bet to consider.
    """

    def __init__(self, sport: str, bet_type: int) -> None:
        self.sport = sport
        self.bet_type = bet_type

    def scan_market(self) -> dict:
        """
        Scans the sports betting market for arbitrage opportunities.

        Return:
        -------
        A dictionary containing the sport and corresponding arbitrage
        opportunities.
        """
        scrapers = ScrapersPool(self.sport, self.bet_type)
        scrapers.get_data()
        data = scrapers.data
        data.create_events_table()
        arbitrage_obj = Arbitrage(data)
        opportunities = arbitrage_obj.calculate_arbitage()
        return {self.sport: opportunities}
