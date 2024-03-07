

class StreamData:
    
    class StreamIterator:

        def __init__(self, stream_sequence):
            self.__index = 0
            self.__count = len(stream_sequence)
            self.stream_sequence = stream_sequence
            
        
        def __iter__(self):
            return self
        
        def __next__(self):
            if self.__index < self.__count:
                item = self.stream_sequence[self.__index]
                self.__index += 1
                return item
            else:
                raise StopIteration


    def __init__(self, data):
        self.data = self.__validate_data(data)

    # data type -> [(x1, y1, ...), (x2, y2, ...), ...]
    def __validate_data(self, data):
        if  isinstance(data, list) and \
            all(map(lambda element: isinstance(element, tuple), data)) and \
            len(list(filter(lambda element: len(element) == len(data[0]), data))) == len(data):
                return data
        else:
            raise TypeError("Data Type has to be a list of same length tuples")

    def get_stream_iterator(self):
        return self.StreamIterator(self.data)
            



    