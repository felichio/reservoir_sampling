from event.event import EventType
import math


class StreamBuffer:

    def __init__(self, dimension):
        self.dimension = dimension
        
        self.clear_state()

    
    def clear_state(self):
        self.buffer = []
        

        # statistics
        self.mean = [0.0 for _ in range(self.dimension)]
        self.variance = [0.0 for _ in range(self.dimension)]
        self.coefficientvar = [0.0 for _ in range(self.dimension)]

        self.mean_snapshots = []
        self.variance_snapshots = []
        self.coefficientvar_snapshots = []

        # previous step
        self.mean_pre = [0.0 for _ in range(self.dimension)]
        self.variance_pre = [0.0 for _ in range(self.dimension)]

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

    def calculate_coefficientvar(self):
        for i in range(self.dimension):
            self.coefficientvar[i] = math.sqrt(self.variance[i]) / self.mean[i]


    def snap(self):
        self.mean_snapshots.append(self.mean[:])
        self.variance_snapshots.append(self.variance[:])
        self.coefficientvar_snapshots.append(self.coefficientvar[:])

    def consume(self, event):
        if event.event_type == EventType.ITEM_RCV:
            self.buffer.append(event.payload["value"])
            print(f"StreamBuffer consuming {event.event_type} with payload {event.payload}")

            # Calculate stats
            self.calculate_mean(event.payload["value"])
            self.calculate_variance(event.payload["value"])
            self.calculate_coefficientvar()

            # Take snaps
            self.snap()

            print("---- Stream stats ----")
            print("mean: ", self.mean)
            print("variance: ", self.variance)
            print("coefficient_var: ", self.coefficientvar)
        
        
        
    