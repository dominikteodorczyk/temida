from scrapers.fortuna import FortunaTwoWayBets,FortunaThreeWayBets
from utils.sports import Fortuna


def main():
    FortunaThreeWayBets(Fortuna().football).get_events_values()

if __name__ == "__main__":
    main()