"""
Module: events_types

This module defines classes and dictionaries representing different
sports and their corresponding bet types for sports betting scrapers.

Classes:
--------
1. EventsTypes: A class defining different sports and their corresponding
    bet types.

Dictionaries:
-------------
1. ScrapersDict: A dictionary mapping bookmakers to their
    corresponding scraper classes.
"""

from scrapers.betclic import BetclicTwoWayBets, BetclicThreeWayBets
from scrapers.sts import STSTwoWayBets, STSThreeWayBets
from scrapers.superbet import SuperbetTwoWayBets, SuperbetThreeWayBets
from scrapers.fortuna import FortunaTwoWayBets, FortunaThreeWayBets


class EventsTypes:
    """
    Class representing various sports and their corresponding bet types.

    Attributes:
    -----------
    sports (dict): A dictionary mapping sports to their bet types.

    Note:
    -----
    The sports dictionary is intended to be used by other modules to
    retrieve bet types for specific sports.
    """

    def __init__(self) -> None:
        self.sports = {
            "football": 3,
            "hokey": 3,
            "tennis": 2,
            "basketball": 3,
            "volleyball": 2,
            "handball": 3,
            "mma": 2,
            "boxing": 3,
            "baseball": 3,
            "rugby": 3,
            "table_tennis": 2,
            "futsal": 3,
            "snooker": 2,
        }


class ScrapersDict:
    """
    Class representing a dictionary of bookmakers and their corresponding
    scraper classes.

    Attributes:
    -----------
    scrapers (dict): A dictionary mapping bookmakers to lists of scraper
    classes.

    Note:
    -----
    The scrapers dictionary is intended to be used by other modules
    to retrieve scraper classes for specific bookmakers.
    """

    def __init__(self) -> None:
        self.scrapers = {
            STS(): [STSTwoWayBets, STSThreeWayBets],
            Fortuna(): [FortunaTwoWayBets, FortunaThreeWayBets],
            Betclic(): [BetclicTwoWayBets, BetclicThreeWayBets],
            Superbet(): [SuperbetTwoWayBets, SuperbetThreeWayBets],
        }


class STS:
    """
    Class representing the STS bookmaker and its legal status, along with
    URLs for different sports.
    """

    def __init__(self) -> None:
        self.legal = True
        self.football = (
            "https://www.sts.pl/zaklady-bukmacherskie/pilka-nozna/184"
        )
        self.hokey = (
            "https://www.sts.pl/zaklady-bukmacherskie/hokej-na-lodzie/188"
        )
        self.tennis = "https://www.sts.pl/zaklady-bukmacherskie/tenis/185"
        self.basketball = (
            "https://www.sts.pl/zaklady-bukmacherskie/koszykowka/186"
        )
        self.volleyball = (
            "https://www.sts.pl/zaklady-bukmacherskie/siatkowka/183"
        )
        self.handball = (
            "https://www.sts.pl/zaklady-bukmacherskie/pilka-reczna/187"
        )
        self.mma = "https://www.sts.pl/zaklady-bukmacherskie/sporty-walki/211"
        self.boxing = "https://www.sts.pl/zaklady-bukmacherskie/boks/206"
        self.baseball = None
        self.rugby = "https://www.sts.pl/zaklady-bukmacherskie/rugby/195"
        self.table_tennis = (
            "https://www.sts.pl/zaklady-bukmacherskie/tenis-stolowy/209"
        )
        self.futsal = "https://www.sts.pl/zaklady-bukmacherskie/futsal/192"
        self.snooker = "https://www.sts.pl/zaklady-bukmacherskie/snooker/198"


class Fortuna:
    """
    Class representing the Fortuna bookmaker and its legal status, along with
    URLs for different sports.
    """

    def __init__(self) -> None:
        self.legal = True
        self.football = (
            "https://www.efortuna.pl/zaklady-bukmacherskie/pilka-nozna"
        )
        self.hokey = "https://www.efortuna.pl/zaklady-bukmacherskie/hokej"
        self.tennis = "https://www.efortuna.pl/zaklady-bukmacherskie/tenis"
        self.basketball = (
            "https://www.efortuna.pl/zaklady-bukmacherskie/koszykowka"
        )
        self.volleyball = (
            "https://www.efortuna.pl/zaklady-bukmacherskie/siatkowka"
        )
        self.handball = (
            "https://www.efortuna.pl/zaklady-bukmacherskie/pilka-reczna"
        )
        self.mma = "https://www.efortuna.pl/zaklady-bukmacherskie/mma"
        self.boxing = "https://www.efortuna.pl/zaklady-bukmacherskie/boks"
        self.baseball = (
            "https://www.efortuna.pl/zaklady-bukmacherskie/baseball"
        )
        self.rugby = "https://www.efortuna.pl/zaklady-bukmacherskie/rugby"
        self.table_tennis = (
            "https://www.efortuna.pl/zaklady-bukmacherskie/tenis-stolowy"
        )
        self.futsal = "https://www.efortuna.pl/zaklady-bukmacherskie/futsal"
        self.snooker = "https://www.efortuna.pl/zaklady-bukmacherskie/snooker"


class Betclic:
    """
    Class representing the Betclic bookmaker and its legal status, along with
    URLs for different sports.
    """

    def __init__(self) -> None:
        self.legal = True
        self.football = "https://www.betclic.pl/pilka-nozna-s1"
        self.hokey = "https://www.betclic.pl/hokej-s13"
        self.tennis = "https://www.betclic.pl/tenis-s2"
        self.basketball = "https://www.betclic.pl/koszykowka-s4"
        self.volleyball = "https://www.betclic.pl/siatkowka-s8"
        self.handball = "https://www.betclic.pl/pilka-reczna-s9"
        self.mma = "https://www.betclic.pl/sztuki-walki-s23"
        self.boxing = "https://www.betclic.pl/boks-s16"
        self.baseball = None
        self.rugby = "https://www.betclic.pl/rugby-xv-s5"
        self.table_tennis = None
        self.futsal = "https://www.betclic.pl/futsal-s56"
        self.snooker = "https://www.betclic.pl/snooker-s54"


class Superbet:
    """
    Class representing the Superbet bookmaker and its legal status, along with
    URLs for different sports.
    """

    def __init__(self) -> None:
        self.legal = True
        self.football = "https://superbet.pl/zaklady-bukmacherskie/pilka-nozna"
        self.hokey = (
            "https://superbet.pl/zaklady-bukmacherskie/hokej-na-lodzie"
        )
        self.tennis = "https://superbet.pl/zaklady-bukmacherskie/tenis"
        self.basketball = (
            "https://superbet.pl/zaklady-bukmacherskie/koszykowka"
        )
        self.volleyball = "https://superbet.pl/zaklady-bukmacherskie/siatkowka"
        self.handball = (
            "https://superbet.pl/zaklady-bukmacherskie/pilka-reczna"
        )
        self.mma = "https://superbet.pl/zaklady-bukmacherskie/sporty-walki"
        self.boxing = "https://superbet.pl/zaklady-bukmacherskie/boks"
        self.baseball = "https://superbet.pl/zaklady-bukmacherskie/baseball"
        self.rugby = "https://superbet.pl/zaklady-bukmacherskie/rugby"
        self.table_tennis = (
            "https://superbet.pl/zaklady-bukmacherskie/tenis-stolowy"
        )
        self.futsal = "https://superbet.pl/zaklady-bukmacherskie/futsal"
        self.snooker = None


class Forbet:
    """
    Class representing the Forbet bookmaker and its legal status, along with
    URLs for different sports.
    """

    def __init__(self) -> None:
        self.legal = True
        self.football = "https://www.iforbet.pl/zaklady-bukmacherskie/1"
        self.hokey = "https://www.iforbet.pl/zaklady-bukmacherskie/4"
        self.tennis = "https://www.iforbet.pl/zaklady-bukmacherskie/5"
        self.basketball = "https://www.iforbet.pl/zaklady-bukmacherskie/2"
        self.volleyball = "https://www.iforbet.pl/zaklady-bukmacherskie/10"
        self.handball = "https://www.iforbet.pl/zaklady-bukmacherskie/6"
        self.mma = "https://www.iforbet.pl/zaklady-bukmacherskie/41"
        self.boxing = "https://www.iforbet.pl/zaklady-bukmacherskie/40"
        self.baseball = "https://www.iforbet.pl/zaklady-bukmacherskie/3"
        self.rugby = "https://www.iforbet.pl/zaklady-bukmacherskie/12"
        self.table_tennis = "https://www.iforbet.pl/zaklady-bukmacherskie/20"
        self.futsal = None
        self.snooker = "https://www.iforbet.pl/zaklady-bukmacherskie/19"
