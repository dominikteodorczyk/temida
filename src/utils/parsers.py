from datetime import datetime, timedelta


class Parser:
    @staticmethod
    def parse_home_win(odds_str):
        return float(odds_str.replace(",", "."))

    @staticmethod
    def parse_draw(odds_str):
        return float(odds_str.replace(",", "."))

    @staticmethod
    def parse_away_win(odds_str):
        return float(odds_str.replace(",", "."))


class FortunaParser(Parser):
    @staticmethod
    def parse_date(date_str):
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
        if date_str == "Dzisiaj":
            return datetime.now().strftime("%Y-%m-%d")
        else:
            return datetime.strptime(f"{date_str}", "%d.%m.%Y").date()

    @staticmethod
    def parse_event_name(*args):
        return f"{args[0].strip()} - {args[1].strip()}"

    @staticmethod
    def parse_home_name(home_name):
        return home_name.strip().upper()

    @staticmethod
    def parse_away_name(away_name):
        return away_name.strip().upper()


class BetclicParser(Parser):
    @staticmethod
    def parse_date(date_str):
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
        return f"{args[0].strip()} - {args[1].strip()}"

    @staticmethod
    def parse_home_name(home_name):
        return home_name.strip().upper()

    @staticmethod
    def parse_away_name(away_name):
        return away_name.strip().upper()


class SuperbetParser(Parser):
    @staticmethod
    def parse_date(date_str):
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
        return f"{args[0].strip()} - {args[1].strip()}"

    @staticmethod
    def parse_home_name(home_name):
        return home_name.strip().upper()

    @staticmethod
    def parse_away_name(away_name):
        return away_name.strip().upper()

