import threading
from input.stream_data import StreamData
from event.event import Event
from event.event import EventType
from input.csv_reader import CsvReader
from event.event_queue import EventQueue
from consumer.stream_buffer import StreamBuffer
from consumer.reservoir_buffer import ReservoirBuffer
from consumer.era_handler import EraHandler

data = [(1, 2), (3, 4), (5, 6), (7, 9)]


def main():
    eq = EventQueue()

    # Start the queue thread
    qt = threading.Thread(target = eq.run, args = (), daemon = True)
    qt.start()

    
    values = CsvReader("src/input/simple.csv").values_d([1, 2, 3, 4, 5])
    head = CsvReader("src/input/simple.csv").head_d([1, 2, 3, 4, 5])
    print(head)
    dimension = len(values[0])

    sb = StreamBuffer(dimension)
    rb = ReservoirBuffer(2, dimension)
    eh = EraHandler(sb, rb)
    eq.subscribe(EventType.ITEM_RCV, sb)
    eq.subscribe(EventType.ITEM_RCV, rb)
    eq.subscribe(EventType.EOS, eh)
    rb.register_era_handler(eh)

    sdd = StreamData(values)
    for i, item in enumerate(sdd.get_stream_iterator()):
        eq.enqueue(Event.create_itemrcv(i + 1, item))

    # send EOS event
    eq.enqueue(Event.create_eos())

    

    qt.join()
    print(eh.eras[-1].reservoir_buffer_mean)
    print(eh.eras[-1].reservoir_buffer_variance)
    



if __name__ == "__main__":
    main()