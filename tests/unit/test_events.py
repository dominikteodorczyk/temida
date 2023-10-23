import os
import pytest
import pandas as pd
from utils.events import MainEventsBoard


class Test_MainEventsBoard:
    @pytest.fixture
    def data_dir(self):
        return os.path.join(os.getcwd(), "tests", "data")

    @pytest.fixture
    def fortuna_board(self, data_dir):
        return pd.read_csv(os.path.join(data_dir, "fortuna_data.csv"))

    @pytest.fixture
    def sts_board(self, data_dir):
        return pd.read_csv(os.path.join(data_dir, "sts_data.csv"))

    @pytest.fixture
    def betclic_board(self, data_dir):
        return pd.read_csv(os.path.join(data_dir, "betclic_data.csv"))

    @pytest.fixture
    def superbet_board(self, data_dir):
        return pd.read_csv(os.path.join(data_dir, "superbet_data.csv"))

    def test_MainEventsBoard_have_events_dict_atribut_as_list(self):
        atributes = vars(MainEventsBoard())
        assert type(atributes["events_dict"]) == dict

    def test_MainEventsBoard_have_events_table_atribut_as_DataFrame(self):
        atributes = vars(MainEventsBoard())
        assert type(atributes["events_table"]) == pd.DataFrame

    def test_MainEventsBoard_put_data_append_data_to_list(
        self, fortuna_board, sts_board
    ):
        obj = MainEventsBoard()
        obj.put_data(fortuna_board)
        assert len(obj.events_dict) == 1
        obj.put_data(sts_board)
        assert len(obj.events_dict) == 2
