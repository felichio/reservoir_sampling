import threading
from input.stream_data import StreamData
from event.event import Event
from event.event import EventType
from input.csv_reader import CsvReader
from event.event_queue import EventQueue
from consumer.stream_buffer import StreamBuffer
from consumer.reservoir_buffer import ReservoirBuffer

data = [(1, 2), (3, 4), (5, 6), (7, 9)]


def main():
    eq = EventQueue()

    # Start the queue thread
    qt = threading.Thread(target = eq.run, args = (), daemon = True)
    qt.start()

    
    values = CsvReader("src/input/simple.csv").values()
    head = CsvReader("src/input/simple.csv").head_d([1])
    
    sb = StreamBuffer()
    rb = ReservoirBuffer(10)
    eq.subscribe(EventType.ITEM_RCV, sb)
    eq.subscribe(EventType.ITEM_RCV, rb)

    sdd = StreamData(values)
    for i, item in enumerate(sdd.get_stream_iterator()):
        eq.enqueue(Event.create_itemrcv(i + 1, item))

    # send EOS event
    eq.enqueue(Event.create_eos())

    qt.join()
    



if __name__ == "__main__":
    main()