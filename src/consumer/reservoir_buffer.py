import random
import math
from event.event import EventType


class ReservoirBuffer:


    def __init__(self, size, dimension):
        self.size = size
        self.dimension = dimension
        
        self.clear_state()

    def clear_state(self):
        self.buffer = []
        self.buffer_snapshots = []


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

    def calculate_mean(self, removed_value, inserted_value):
        n = self.size
        # snap the previous step mean values
        self.mean_pre = self.mean[:]
        # calculate the new ones
        for i in range(self.dimension):
            self.mean[i] = self.mean[i] + (inserted_value[i] - removed_value[i]) / n

    def calculate_variance(self, removed_value, inserted_value):
        n = self.size
        # snap the previous step variance values
        self.variance_pre = self.variance[:]
        # calculate the new ones
        for i in range(self.dimension):
            self.variance[i] = self.variance[i] + (inserted_value[i] ** 2 - removed_value[i] ** 2) / n + self.mean_pre[i] ** 2 - self.mean[i] ** 2

    def calculate_coefficientvar(self):
        for i in range(self.dimension):
            self.coefficientvar[i] = math.sqrt(self.variance[i]) / self.mean[i]

    def snap(self, diff):
        if diff:
            self.buffer_snapshots.append(self.buffer[:])
            self.mean_snapshots.append(self.mean[:])
            self.variance_snapshots.append(self.variance[:])
            self.coefficientvar_snapshots.append(self.coefficientvar[:])
        else:
            self.buffer_snapshots.append(["-"])
            self.mean_snapshots.append(["-"])
            self.variance_snapshots.append(["-"])
            self.coefficientvar_snapshots.append(["-"])

    def consume(self, event):
        if event.event_type == EventType.ITEM_RCV:
            print(f"ReservoirBuffer consuming {event.event_type} with payload {event.payload}")
            if len(self.buffer) < self.size:
                self.buffer.append(event.payload["value"])
                # Copy the streams moving statistics
                self.mean_pre = self.era_handler.stream_buffer.mean_pre[:]
                self.mean = self.era_handler.stream_buffer.mean[:]
                self.variance_pre = self.era_handler.stream_buffer.variance_pre[:]
                self.variance = self.era_handler.stream_buffer.variance[:]

                self.coefficientvar = self.era_handler.stream_buffer.coefficientvar[:]

                # Take then snapshots
                self.snap(True)
            else:
                # Run AlgorithmR
                print("Running AlgorithR")
                # take number of stream elements seen
                n = len(self.era_handler.stream_buffer.buffer)
                index = ReservoirBuffer.R(n, self.size)
                print("index: ", index)
                if index < self.size:
                    # save removed value
                    removed_value = self.buffer[index]
                    inserted_value = event.payload["value"]
                    # swap new with old
                    self.buffer[index] = inserted_value
                    # calculate new buffer statistics
                    self.calculate_mean(removed_value, inserted_value)
                    self.calculate_variance(removed_value, inserted_value)
                    self.calculate_coefficientvar()

                    # Take snaps
                    self.snap(True)

                    # check era handler
                    pass
                else:
                    self.snap(False)
                    pass

            print("---- Reservoir stats ----")
            print("Reservoir: ", self.buffer)        
            print("mean: ", self.mean)
            print("variance: ", self.variance)
            print("coefficient_var: ", self.coefficientvar)


    def register_era_handler(self, era_handler):
        self.era_handler = era_handler


    @staticmethod
    def R(n, capacity):
        return random.randint(0, n - 1)
        

    