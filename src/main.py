from input.stream_data import StreamData
from event.event import Event

data = [(1, 2), (3, 4), (5, 6), (7, 9)]


def main():
    sd = StreamData(data)
    queue = []
    
    for i, item in enumerate(sd.get_stream_iterator()):
        ev = Event.create_itemrcv(i + 1, item)
        queue.append(ev)

    for ev in queue:
        print(ev.payload)
    



if __name__ == "__main__":
    main()