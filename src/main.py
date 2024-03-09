from input.stream_data import StreamData
from event.event import Event
from event.event import EventType
from input.csv_reader import CsvReader
from event.event_queue import EventQueue
from consumer.dummy import Dummy

data = [(1, 2), (3, 4), (5, 6), (7, 9)]


def main():
    sd = StreamData(data)
    queue = []

    for i, item in enumerate(sd.get_stream_iterator()):
        ev = Event.create_itemrcv(i + 1, item)
        queue.append(ev)

    
    
    values = CsvReader("src/input/simple.csv").values_d([1, 2, 2, 1])
    head = CsvReader("src/input/simple.csv").head_d([1, 2, 3, 4, 5])
    
    sdd = StreamData(values)
    for i, item in enumerate(sdd.get_stream_iterator()):
        ev = Event.create_itemrcv(i + 1, item)
        queue.append(ev)
        print(ev.event_type, ev.payload)

    eq = EventQueue()
    dummy1 = Dummy()
    dummy2 = Dummy()
    eq.subscribe(EventType.ITEM_RCV, dummy1)
    eq.subscribe(EventType.ITEM_RCV, dummy2)
    eq.dispatch(Event.create_itemrcv(10, 100))



if __name__ == "__main__":
    main()