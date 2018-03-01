from collections import namedtuple

Ride = namedtuple("Ride", ["start", "finish", "start_time", "end_time"])


def read_input(stream):
    num_rows, num_cols, num_vehicles, num_rides, bonus, num_steps = list(map(int, stream.readline().split()()))
    rides = []
    for _ in range(num_rides):
        a, b, x, y, s, f = list(map(int, stream.readline().split()))
        rides.append(Ride((a, b), (x, y), s, f))
    return num_rows, num_cols, num_vehicles, num_rides, bonus, num_steps, rides


def score(num_rows, num_cols, num_vehicles, num_rides, bonus, num_steps, rides, rides_by_vehicle):
    total_score = 0
    for v in range(num_vehicles):
        current_rides = rides_by_vehicle[v]
        current_time = 0
        for rid in current_rides:
            ride = rides[rid]






def read_output(stream):
    rides_by_vehicle = []
    for line in stream:
        tokens = list(map(int, line.split()))
        n_rides = tokens[0]
        assert(len(tokens[1:]) == n_rides)
        rides_by_vehicle.append(tokens[1:])
    return rides_by_vehicle