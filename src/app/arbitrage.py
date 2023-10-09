from utils.events import *

class Arbitrage:
    #TODO: clasa wykonująca arbitraż na całej tablicy
    def __init__(self, data_object: MainEventsBoard) -> None:
        self.data_object = data_object
        self_arbitrage_pair = DataFrame()

    def calculate_arbitage(self):
        for index, row in self.data_object.events_table.iterrows():
            event = Event.create(row,self.data_object.events_dict)
    

class EventArbitrage:
    def __init__(self, event_object: Event, event_results) -> None:
        self.event_object = event_object
        self.event_results = event_results

    @classmethod
    def create(cls, event_object: Event):
        event_results['event_name'] = event_object[1]['event_name']
        event_results['event_date'] = event_object[1]['event_date']
        return cls(event_object, event_results)

    
