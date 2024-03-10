


class StreamBuffer:

    def __init__(self, dimension):
        self.dimension = dimension
        self.buffer = []
        

        # statistics
        self.mean = [0.0 for _ in range(dimension)]
        self.variance = [0.0 for _ in range(dimension)]

        # previous step
        self.mean_pre = [0.0 for _ in range(dimension)]
        self.variance_pre = [0.0 for _ in range(dimension)]

    def calculate_mean(self, inserted_value):
        n = len(self.buffer)
        # snap the previous step mean values
        self.mean_pre = self.mean[:]
        # calculate the new ones
        for i in range(self.dimension):
            # moving average
            self.mean[i] = (n - 1) / n * self.mean[i] + 1 / n * inserted_value[i]


    def calculate_variance(self, inserted_value):
        n = len(self.buffer)
        for i in range(self.dimension):
            self.variance[i] = (n - 1) / n * self.variance[i] + (n - 1) / (n ** 2) * (inserted_value[i] - self.mean_pre[i]) ** 2


    def consume(self, event):
        self.buffer.append(event.payload["value"])
        print(f"StreamBuffer consuming {event.event_type} with payload {event.payload}")

        # Calculate stats
        self.calculate_mean(event.payload["value"])
        self.calculate_variance(event.payload["value"])
        print("---- Stream stats ----")
        print("mean: ", self.mean)
        print("variance: ", self.variance)
        
        
        
    