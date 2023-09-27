from scrapers.betclic import BetclicThreeWayBets
from utils.sports import Betclic


def main():
    drvr = BetclicThreeWayBets(Betclic().football).get_events_values()


if __name__ == "__main__":
    main()
