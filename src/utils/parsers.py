from datetime import datetime

class Parser:

    @staticmethod
    def parse_home_win(odds_str):
        return float(odds_str)

    @staticmethod
    def parse_draw(odds_str):
        return float(odds_str)

    @staticmethod
    def parse_away_win(odds_str):
        return float(odds_str)

class STSParsers:

    def __init__(self) -> None:
        pass

    def parse_home(self,home_name:str) -> str:
        components = home_name.split()
        return max(components, key=len).strip().upper()

    def parse_away(self,away_name:str) -> str:
        components = away_name.split()
        return max(components, key=len).strip().upper()

    def parse_date(self,event_date:str) -> str:
        pass

    def parse_event_code(self,even_name:str,event_date:str) -> str:
        pass

class FortunaParser(Parser):

    @staticmethod
    def parse_date(date_str):
        return datetime.strptime(f"{date_str}.{datetime.now().year}", "%d.%m.%Y")

    @staticmethod
    def parse_event_name(event_name):
        return event_name.strip()

    @staticmethod
    def parse_home_name(event_name):
        return event_name.split(" - ")[0].strip().upper()

    @staticmethod
    def parse_away_name(event_name):
        return event_name.split(" - ")[1].strip().upper()

# :TODO: propozycja algorytmu najdującego podobieństwo
# def jaccard_similarity(s1, s2):
#     set1 = set(s1)
#     set2 = set(s2)
#     intersection = len(set1.intersection(set2))
#     union = len(set1) + len(set2) - intersection
#     similarity = intersection / union
#     return similarity

# napis1 = "Napoli - Real M."
# napis2 = [
#     'Union - Berlin Braga',
# 'Salzburg - Real Sociedad',
# 'PSV - Sevilla',
# 'Lens - Arsenal',
# 'FC Kopenhaga - Bayern',
# 'Man. Utd - Galatasaray',
# 'Napoli - Real Madryt',
# 'Inter - Benfica',
# 'Antwerp - Sz. Donieck',
# 'Atl. Madryt - Feyenoord',
# 'Crvena Zvezda - Young Boys',
# 'RB Lipsk - Man. City',
# 'Celtic - Lazio',
# 'Dortmund - Milan',
# 'Newcastle - PSG',
# 'FC Porto - Barcelona',
# 'Marsylia - Brighton',
# 'Aris - Limassol Rangers',
# 'Sp. Lizbona - Atalanta',
# 'Backa Topola - Olympiakos',
# 'AEK Ateny - Ajax',
# 'Freiburg - West Ham',
# 'Betis - Sparta Praga',
# 'Raków - Sturm Graz',
# 'Liverpool - St. Gilloise',
# 'Maccabi Haifa - Panathinaikos',
# 'Villarreal - Rennes',
# 'Toulouse - LASK Linz',
# 'Molde - Leverkusen',
# 'Hacken - Qarabag',
# 'Roma - Servette',
# 'Slavia Praga - Sheriff Tiraspol',
# 'Astana - Vik. Pilzno',
# ]
# ratio = 0
# best = []
# for i in napis2:
#     podobienstwo = jaccard_similarity(napis1, i)
#     if podobienstwo > ratio:
#         best = [i,podobienstwo]
#         ratio = podobienstwo

# print best

# potrafi połączyć 'Crvena Zvezda - Young Boys' z 'CZ Belgrad - YB Bern'

import pandas as pd
from datetime import datetime

class Parser:
    @staticmethod
    def parse_date(date_str):
        return datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")

    @staticmethod
    def parse_event_name(home_team, away_team):
        if home_team and away_team:
            return f"{home_team} vs {away_team}"
        elif home_team:
            return f"{home_team} Match"
        elif away_team:
            return f"{away_team} Match"
        else:
            return "Unknown Event"

    @staticmethod
    def parse_odds(odds_str):
        return float(odds_str)

class Event:
    def __init__(self, event_name, home_team, away_team, date, odds_win, odds_loss):
        self.event_name = event_name
        self.home_team = home_team
        self.away_team = away_team
        self.date = date
        self.odds_win = odds_win
        self.odds_loss = odds_loss

    def __str__(self):
        return f"{self.event_name}: {self.home_team} vs {self.away_team}, Date: {self.date}, Win Odds: {self.odds_win}, Loss Odds: {self.odds_loss}"

    def to_dataframe(self):
        data = {
            'Event Name': [self.event_name],
            'Home Team': [self.home_team],
            'Away Team': [self.away_team],
            'Date': [self.date],
            'Win Odds': [self.odds_win],
            'Loss Odds': [self.odds_loss]
        }
        return pd.DataFrame(data)

    @classmethod
    def create_from_bukmacher_data(cls, bukmacher_data, parser):
        home_team = bukmacher_data.get('home_team', None)
        away_team = bukmacher_data.get('away_team', None)
        event_name = bukmacher_data.get('event_name', None) or parser.parse_event_name(home_team, away_team)

        date = parser.parse_date(bukmacher_data['date'])
        odds_win = parser.parse_odds(bukmacher_data['odds_win'])
        odds_loss = parser.parse_odds(bukmacher_data['odds_loss'])

        return cls(event_name, home_team, away_team, date, odds_win, odds_loss)

# Przykład użycia
bukmacher_data = {
    'event_name': 'Special Event',
    'home_team': 'PlayerX',
    'away_team': 'PlayerY',
    'date': '2023-09-28 18:30:00',
    'odds_win': '1.8',
    'odds_loss': '2.2'
}

parser = Parser()
event = Event.create_from_bukmacher_data(bukmacher_data, parser)

# Przekształcenie obiektu do DataFrame
df = event.to_dataframe()
print(df)
