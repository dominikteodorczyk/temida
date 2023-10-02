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
        today = datetime.now().date()
        if today.month >= datetime.strptime(date_str, "%d.%m.%Y").month:
            return datetime.strptime(f"{date_str}.{datetime.now().year}", "%d.%m.%Y")
        else:
            return datetime.strptime(f"{date_str}.{datetime.now().year + 1}", "%d.%m.%Y")

    @staticmethod
    def parse_event_n_names(*args):
        return args[0].strip()

    @staticmethod
    def parse_home_name(event_name):
        return event_name.split(" - ")[0].strip().upper()

    @staticmethod
    def parse_away_name(event_name):
        return event_name.split(" - ")[1].strip().upper()


class STSParser(Parser):

    @staticmethod
    def parse_date(date_str):
        return datetime.strptime(f"{date_str}", "%d.%m.%Y")

    @staticmethod
    def parse_event_n_names(*args):
        return f'{args[0].strip()} - {args[1].strip()}'

    @staticmethod
    def parse_home_name(home_name):
        return home_name.strip().upper()

    @staticmethod
    def parse_away_name(away_name):
        return away_name.strip().upper()



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
