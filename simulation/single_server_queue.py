import math
import random

class SingleServerQueue:
    Q_LIMIT = 100
    BUSY = 1
    IDLE = 0
    MODLUS = 2147483647
    MULT1 = 24112
    MULT2 = 26143

    def __init__(self, mean_interarrival, mean_service, num_delays_required):
        self.mean_interarrival = mean_interarrival
        self.mean_service = mean_service
        self.num_delays_required = num_delays_required

        self.sim_time = 0.0
        self.server_status = self.IDLE
        self.num_in_q = 0
        self.time_last_event = 0.0
        self.num_custs_delayed = 0
        self.total_of_delays = 0.0
        self.area_num_in_q = 0.0
        self.area_server_status = 0.0
        self.time_next_event = [0.0, 0.0, 0.0]
        self.time_arrival = [0.0] * (self.Q_LIMIT + 1)
        self.zrng = [1,
                     1973272912, 281629770, 20006270, 1280689831, 2096730329, 1933576050,
                     913566091, 246780520, 1363774876, 604901985, 1511192140, 1259851944,
                     824064364, 150493284, 242708531, 75253171, 1964472944, 1202299975,
                     233217322, 1911216000, 726370533, 403498145, 993232223, 1103205531,
                     762430696, 1922803170, 1385516923, 76271663, 413682397, 726466604,
                     336157058, 1432650381, 1120463904, 595778810, 877722890, 1046574445,
                     68911991, 2088367019, 748545416, 622401386, 2122378830, 640690903,
                     1774806513, 2132545692, 2079249579, 78130110, 852776735, 1187867272,
                     1351423507, 1645973084, 1997049139, 922510944, 2045512870, 898585771,
                     243649545, 1004818771, 773686062, 403188473, 372279877, 1901633463,
                     498067494, 2087759558, 493157915, 597104727, 1530940798, 1814496276,
                     536444882, 1663153658, 855503735, 67784357, 1432404475, 619691088,
                     119025595, 880802310, 176192644, 1116780070, 277854671, 1366580350,
                     1142483975, 2026948561, 1053920743, 786262391, 1792203830, 1494667770,
                     1923011392, 1433700034, 1244184613, 1147297105, 539712780, 1545929719,
                     190641742, 1645390429, 264907697, 620389253, 1502074852, 927711160,
                     364849192, 2049576050, 638580085, 547070247]
        self.num_events = 2
        self.initialize()

    def lcgrand(self, stream):
        zi = self.zrng[stream]
        lowprd = (zi & 65535) * self.MULT1
        hi31 = (zi >> 16) * self.MULT1 + (lowprd >> 16)
        zi = ((lowprd & 65535) - self.MODLUS) + ((hi31 & 32767) << 16) + (hi31 >> 15)
        if zi < 0:
            zi += self.MODLUS
        lowprd = (zi & 65535) * self.MULT2
        hi31 = (zi >> 16) * self.MULT2 + (lowprd >> 16)
        zi = ((lowprd & 65535) - self.MODLUS) + ((hi31 & 32767) << 16) + (hi31 >> 15)
        if zi < 0:
            zi += self.MODLUS
        self.zrng[stream] = zi
        return ((zi >> 7) | 1) / 16777216.0

    def initialize(self):
        self.sim_time = 0.0
        self.server_status = self.IDLE
        self.num_in_q = 0
        self.time_last_event = 0.0
        self.num_custs_delayed = 0
        self.total_of_delays = 0.0
        self.area_num_in_q = 0.0
        self.area_server_status = 0.0
        self.time_next_event[1] = self.sim_time + self.expon(self.mean_interarrival)
        self.time_next_event[2] = 1.0e+30

    def timing(self):
        min_time_next_event = 1.0e+29
        self.next_event_type = 0

        for i in range(1, self.num_events + 1):
            if self.time_next_event[i] < min_time_next_event:
                min_time_next_event = self.time_next_event[i]
                self.next_event_type = i

        if self.next_event_type == 0:
            print(f"Event list empty at time {self.sim_time}")
            exit(1)

        self.sim_time = min_time_next_event

    def arrive(self):
        self.time_next_event[1] = self.sim_time + self.expon(self.mean_interarrival)

        if self.server_status == self.BUSY:
            self.num_in_q += 1

            if self.num_in_q > self.Q_LIMIT:
                print(f"\nOverflow of the array time_arrival at time {self.sim_time}")
                exit(1)

            self.time_arrival[self.num_in_q] = self.sim_time
        else:
            delay = 0.0
            self.total_of_delays += delay
            self.num_custs_delayed += 1
            self.server_status = self.BUSY
            self.time_next_event[2] = self.sim_time + self.expon(self.mean_service)

    def depart(self):
        if self.num_in_q == 0:
            self.server_status = self.IDLE
            self.time_next_event[2] = 1.0e+30
        else:
            self.num_in_q -= 1
            delay = self.sim_time - self.time_arrival[1]
            self.total_of_delays += delay
            self.num_custs_delayed += 1
            self.time_next_event[2] = self.sim_time + self.expon(self.mean_service)

            for i in range(1, self.num_in_q + 1):
                self.time_arrival[i] = self.time_arrival[i + 1]

    def expon(self, mean):
        return -mean * math.log(self.lcgrand(1))

    def update_time_avg_stats(self):
        time_since_last_event = self.sim_time - self.time_last_event
        self.time_last_event = self.sim_time

        self.area_num_in_q += self.num_in_q * time_since_last_event
        self.area_server_status += self.server_status * time_since_last_event

    def report(self):
        avg_delay_in_queue = self.total_of_delays / self.num_custs_delayed
        avg_num_in_queue = self.area_num_in_q / self.sim_time
        server_utilization = self.area_server_status / self.sim_time

        print(f"\n\nAverage delay in queue {avg_delay_in_queue:.3f} minutes")
        print(f"Average number in queue {avg_num_in_queue:.3f}")
        print(f"Server utilization {server_utilization:.3f}")
        print(f"Time simulation ended {self.sim_time:.3f} minutes")

    def run_simulation(self):
        while self.num_custs_delayed < self.num_delays_required:
            self.timing()
            self.update_time_avg_stats()

            if self.next_event_type == 1:
                self.arrive()
            elif self.next_event_type == 2:
                self.depart()

        self.report()


def main():
    mean_interarrival = 1.0  # Mean interarrival time in minutes
    mean_service = 0.5  # Mean service time in minutes
    num_delays_required = 1000  # Number of customers

    ssq = SingleServerQueue(mean_interarrival, mean_service, num_delays_required)
    ssq.run_simulation()


if __name__ == "__main__":
    main()
