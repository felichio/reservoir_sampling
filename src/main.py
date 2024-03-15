import threading
from input.stream_data import StreamData
from event.event import Event
from event.event import EventType
from input.csv_reader import CsvReader
from event.event_queue import EventQueue
from consumer.stream_buffer import StreamBuffer
from consumer.reservoir_buffer import ReservoirBuffer
from consumer.era_handler import EraHandler
from producer.stream_item_generator import StreamItemGenerator
from config.config import settings

input_path = settings["input"]
reservoir_size = settings["reservoir_size"]
columns = settings["columns"]

def main():
    ceq = EventQueue()
    peq = EventQueue()
    print(settings)
    # Start the queue thread
    ceq_thread = threading.Thread(target = ceq.run, args = (), daemon = True)
    ceq_thread.start()

    peq_thread = threading.Thread(target = peq.run, args = (), daemon = True)
    peq_thread.start()

    
    values = CsvReader(input_path).values_d(columns)
    head = CsvReader(input_path).head_d(columns)
    
    dimension = len(values[0])

    sb = StreamBuffer(dimension)
    rb = ReservoirBuffer(reservoir_size, dimension)
    eh = EraHandler(sb, rb)
    ceq.subscribe(EventType.ITEM_RCV, sb)
    ceq.subscribe(EventType.ITEM_RCV, rb)
    ceq.subscribe(EventType.EOS, eh)
    rb.register_era_handler(eh)

    

    sdd = StreamData(values)
    # for i, item in enumerate(sdd.get_stream_iterator()):
        # ceq.enqueue(Event.create_itemrcv(i + 1, item))

    stream_item_gen = StreamItemGenerator(sdd.get_stream_iterator())
    peq.subscribe(EventType.SOS, stream_item_gen)
    peq.subscribe(EventType.EOS, stream_item_gen)
    # send EOS event
    peq.enqueue(Event.create_sos(ceq))
    peq.enqueue(Event.create_eos(ceq))

    

    ceq_thread.join()
    peq_thread.join()
    print(eh.eras[-1].reservoir_variance_snapshots)
    # print(eh.eras[-1].reservoir_mean_snapshots)
    
    



if __name__ == "__main__":
    main()