import time
from app.webscrper import ScrapersPool
import pandas as pd
import os
from utils.events import *
from app.arbitrage import *

def main():
    data_dir = os.path.join(os.getcwd(), "tests", "data")
    fortuna_board = pd.read_csv(os.path.join(data_dir, "fortuna_data.csv"))
    sts_board = pd.read_csv(os.path.join(data_dir, "sts_data.csv"))
    betclic_board = pd.read_csv(os.path.join(data_dir, "betclic_data.csv"))
    superbet_board = pd.read_csv(os.path.join(data_dir, "superbet_data.csv"))
    events = pd.read_csv(os.path.join(data_dir, "merged.csv"))

    sts_obj = ThreeWayBetEventsTable('STS')
    sts_obj.data = sts_board

    fortuna_obj = ThreeWayBetEventsTable('FORTUNA')
    fortuna_obj.data = fortuna_board

    betclic_obj = ThreeWayBetEventsTable('BETCLIC')
    betclic_obj.data = betclic_board

    superbet_obj = ThreeWayBetEventsTable('SUPERBET')
    superbet_obj.data = superbet_board


    main_obj = MainEventsBoard()
    main_obj.put_data(sts_obj)
    main_obj.put_data(fortuna_obj)
    main_obj.put_data(betclic_obj)
    main_obj.put_data(superbet_obj)

    main_obj.events_table = events

    arbitrage_obj = Arbitrage(main_obj)
    arbitrage_obj.calculate_arbitage()

if __name__ == "__main__":
    main()

# 2196 rows x 4 columns
# 1416