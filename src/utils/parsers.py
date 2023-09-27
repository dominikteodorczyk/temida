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

    def parse_home(self,event_name:str) -> str:
        pass

    def parse_away(self,event_name:str) -> str:
        pass

    def parse_date(self,event_date:str) -> str:
        pass

    def parse_event_code(self,even_name:str,event_date:str) -> str:
        pass