from datetime import datetime

class FortunaParsers:

    def __init__(self) -> None:
        pass

    def parse_home(self,event_name:str) -> str:
        components = event_name.split(" - ")[0].strip()
        return max(components.split(), key=len).upper()

    def parse_away(self,event_name:str) -> str:
        components = event_name.split(" - ")[1].strip()
        return max(components.split(), key=len).upper()

    def parse_date(self,event_date:str) -> str:
        return event_date[:5]

    def parse_event_code(self,even_name:str,event_date:str) -> str:
        home = self.parse_home(even_name)[:4]
        away = self.parse_away(even_name)[:4]
        date = self.parse_date(event_date).replace('.','')
        return f'{home}_{away}_{date}'

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