"""
Module Parsers

This module provides a Parser class for handling odds parsing.
"""

from datetime import datetime, timedelta


class Parser:
    """
    A class providing static methods for parsing different types of odds.
    """

    @staticmethod
    def parse_home_win(odds_str):
        """
        Parse home win odds.

        Parameters:
        -----------
        - odds_str (str): The string representing home win odds.

        Returns:
        --------
        float: The parsed home win odds as a float.
        """
        return float(odds_str.replace(",", "."))

    @staticmethod
    def parse_draw(odds_str):
        """
        Parse draw odds.

        Parameters:
        -----------
        - odds_str (str): The string representing draw odds.

        Returns:
        --------
        float: The parsed draw odds as a float.
        """
        return float(odds_str.replace(",", "."))

    @staticmethod
    def parse_away_win(odds_str):
        """
        Parse away win odds.

        Parameters:
        -----------
        - odds_str (str): The string representing away win odds.

        Returns:
        --------
        float: The parsed away win odds as a float.
        """
        return float(odds_str.replace(",", "."))


class FortunaParser(Parser):
    """
    A class providing static methods for parsing odds specific to Fortuna.
    """

    @staticmethod
    def parse_date(date_str):
        """
        Parse the event date from a string.

        Parameters:
        -----------
        - date_str (str): The string representing the event date.

        Returns:
        --------
        datetime.date: The parsed event date.
        """
        today = datetime.now().date()
        if today.month <= datetime.strptime(date_str[:5], "%d.%m").month:
            return datetime.strptime(
                f"{date_str[:5]}.{datetime.now().year}", "%d.%m.%Y"
            ).date()
        else:
            return datetime.strptime(
                f"{date_str[:5]}.{datetime.now().year + 1}", "%d.%m.%Y"
            ).date()

    @staticmethod
    def parse_event_name(*args):
        """
        Parse the event name from input arguments.

        Parameters:
        -----------
        - *args (str): Variable-length arguments representing the event name.

        Returns:
        --------
        str: The parsed event name.
        """
        return args[0].strip()

    @staticmethod
    def parse_home_name(event_name):
        """
        Parse the home team name from the event name.

        Parameters:
        -----------
        - event_name (str): The string representing the event name.

        Returns:
        --------
        str: The parsed home team name.
        """
        return event_name.split(" - ")[0].strip().upper()

    @staticmethod
    def parse_away_name(event_name):
        """
        Parse the away team name from the event name.

        Parameters:
        -----------
        - event_name (str): The string representing the event name.

        Returns:
        --------
        str: The parsed away team name.
        """
        return event_name.split(" - ")[1].strip().upper()


class STSParser(Parser):
    """
    A class providing static methods for parsing odds specific to STS.
    """

    @staticmethod
    def parse_date(date_str):
        """
        Parse the event date from a string.

        Parameters:
        -----------
        - date_str (str): The string representing the event date.

        Returns:
        --------
        datetime.date: The parsed event date.
        """
        if date_str == "Dzisiaj":
            return datetime.now().strftime("%Y-%m-%d")
        else:
            return datetime.strptime(f"{date_str}", "%d.%m.%Y").date()

    @staticmethod
    def parse_event_name(*args):
        """
        Parse the event name from input arguments.

        Parameters:
        -----------
        - *args (str): Variable-length arguments representing the event name.

        Returns:
        --------
        str: The parsed event name.
        """
        return f"{args[0].strip()} - {args[1].strip()}"

    @staticmethod
    def parse_home_name(home_name):
        """
        Parse the home team name from the event name.

        Parameters:
        -----------
        - event_name (str): The string representing the event name.

        Returns:
        --------
        str: The parsed home team name.
        """
        return home_name.strip().upper()

    @staticmethod
    def parse_away_name(away_name):
        """
        Parse the away team name from the event name.

        Parameters:
        -----------
        - event_name (str): The string representing the event name.

        Returns:
        --------
        str: The parsed away team name.
        """
        return away_name.strip().upper()


class BetclicParser(Parser):
    """
    A class providing static methods for parsing odds specific to Betclic.
    """

    @staticmethod
    def parse_date(date_str):
        """
        Parse the event date from a string.

        Parameters:
        -----------
        - date_str (str): The string representing the event date.

        Returns:
        --------
        datetime.date: The parsed event date.
        """
        if date_str == "Dzisiaj":
            return datetime.now().strftime("%Y-%m-%d")
        elif date_str == "Jutro":
            return (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        elif date_str == "Pojutrze":
            return (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d")
        else:
            return datetime.strptime(f"{date_str}", "%d.%m.%Y").date()

    @staticmethod
    def parse_event_name(*args):
        """
        Parse the event name from input arguments.

        Parameters:
        -----------
        - *args (str): Variable-length arguments representing the event name.

        Returns:
        --------
        str: The parsed event name.
        """
        return f"{args[0].strip()} - {args[1].strip()}"

    @staticmethod
    def parse_home_name(home_name):
        """
        Parse the home team name from the event name.

        Parameters:
        -----------
        - event_name (str): The string representing the event name.

        Returns:
        --------
        str: The parsed home team name.
        """
        return home_name.strip().upper()

    @staticmethod
    def parse_away_name(away_name):
        """
        Parse the away team name from the event name.

        Parameters:
        -----------
        - event_name (str): The string representing the event name.

        Returns:
        --------
        str: The parsed away team name.
        """
        return away_name.strip().upper()


class SuperbetParser(Parser):
    """
    A class providing static methods for parsing odds specific to Superbet.
    """

    @staticmethod
    def parse_date(date_str):
        """
        Parse the event date from a string.

        Parameters:
        -----------
        - date_str (str): The string representing the event date.

        Returns:
        --------
        datetime.date: The parsed event date.
        """
        current_date = datetime.now().date()
        if date_str in ["PON.", "WT.", "ŚR.", "CZW.", "PT.", "SOB.", "NIEDZ."]:
            weekday_mapping = {
                "PON.": 0,
                "WT.": 1,
                "ŚR.": 2,
                "CZW.": 3,
                "PT.": 4,
                "SOB.": 5,
                "NIEDZ.": 6,
            }
            days_until_next_weekday = (
                weekday_mapping[date_str] - current_date.weekday() + 7
            ) % 7
            next_weekday = current_date + timedelta(
                days=days_until_next_weekday
            )
            return next_weekday.strftime("%Y-%m-%d")
        else:
            today = datetime.now().date()
            if today.month <= datetime.strptime(date_str, "%d.%m").month:
                return datetime.strptime(
                    f"{date_str}.{datetime.now().year}", "%d.%m.%Y"
                ).date()
            else:
                return datetime.strptime(
                    f"{date_str}.{datetime.now().year + 1}", "%d.%m.%Y"
                ).date()

    @staticmethod
    def parse_event_name(*args):
        """
        Parse the event name from input arguments.

        Parameters:
        -----------
        - *args (str): Variable-length arguments representing the event name.

        Returns:
        --------
        str: The parsed event name.
        """
        return f"{args[0].strip()} - {args[1].strip()}"

    @staticmethod
    def parse_home_name(home_name):
        """
        Parse the home team name from the event name.

        Parameters:
        -----------
        - event_name (str): The string representing the event name.

        Returns:
        --------
        str: The parsed home team name.
        """
        return home_name.strip().upper()

    @staticmethod
    def parse_away_name(away_name):
        """
        Parse the away team name from the event name.

        Parameters:
        -----------
        - event_name (str): The string representing the event name.

        Returns:
        --------
        str: The parsed away team name.
        """
        return away_name.strip().upper()
