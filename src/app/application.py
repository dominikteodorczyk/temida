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
from app.webscrper import ScrapersPool
from app.arbitrage import Arbitrage
from utils.sports import EventsTypes


class MainOperator:
    """
    MainOperator class initializes the application and prints the results.
    This class serves as the main entry point for the application. It
    creates an instance of the DataOperator class to retrieve sports betting
    data, prints the results, and facilitates further processing.
    """

    def __init__(self) -> None:
        reuslts = DataOperator().sort_data()
        print(reuslts)


class DataOperator:

    """
    DataOperator class manages the retrieval of sports betting data.

    This class contains a static method, get_data(), that iterates over
    different sports and bet types, retrieves data using DisciplineOperator,
    and prints the opportunities.
    """

    def __init__(self) -> None:
        self.results = self.get_data()

    def get_data(self):
        """
        Retrieves sports betting data for various sports and bet types.
        """
        opportunities = []
        for sport, bet_type in EventsTypes().sports.items():
            opportunities.append(
                DisciplineOperator(sport, bet_type).scan_market()
            )
        return opportunities

    def sort_data(self):
        twoway = DataFrame()
        threeway = DataFrame()

        for sport_type in self.results:
            sport = next(iter(sport_type.keys()))
            for event in sport_type[sport]:
                if event:
                    event_data = next(iter(event.keys()))
                    event_values = next(iter(event.values()))
                    names_variation = event_values[0]
                    opportunity = event_values[1]

                    if len(opportunity[0]) == 3:
                        for opp in opportunity:
                            i = 1
                            event_to_table = {
                                    'sport':sport,
                                    'event': event_data[0],
                                    "event date": event_data[1],
                                    "1" : opp[[key for key in opp.keys() if key.endswith("home_team_win")][0]],
                                    "X" : opp[[key for key in opp.keys() if key.endswith("draw")][0]],
                                    "2" : opp[[key for key in opp.keys() if key.endswith("away_team_win")][0]]
                                    }
                            for name_variation in names_variation:
                                event_to_table[f'name_{i}'] = name_variation
                                i += 1

                            threeway = threeway._append(event_to_table,ignore_index=True)

                    if len(opportunity[0]) == 2:
                        for opp in opportunity:
                            i = 1
                            event_to_table = {
                                    'sport':sport,
                                    'event': event_data[0],
                                    "event date": event_data[1],
                                    "1" : opp[[key for key in opp.keys() if key.endswith("home_team_win")][0]],
                                    "2" : opp[[key for key in opp.keys() if key.endswith("away_team_win")][0]]
                                    }
                            for name_variation in names_variation:
                                event_to_table[f'name_{i}'] = name_variation
                                i += 1

                            twoway = twoway._append(event_to_table,ignore_index=True)
        return twoway, threeway

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


class MailOperator:
    """
    This class is intended to handle the sending of emails for potential
    betting opportunities. Currently, the implementation is not provided.
    """

    def __init__(self) -> None:
        pass
