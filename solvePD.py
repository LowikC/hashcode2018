import sys
from collections import namedtuple
from PriorityDict import PriorityDict
from tqdm import tqdm

IMPOSSIBLE = 999999999

Ride = namedtuple("Ride", ["id", "start", "finish", "start_time", "finish_time", "latest_start"])

Config = namedtuple("Config", ["num_rows", "num_cols", "num_vehicles", "bonus", "num_steps"])


class VehicleState:
    def __init__(self, pos, step, rides):
        self.pos = pos
        self.step = step
        self.rides = rides


def distance(a, b):
    dx = a[0] - b[0]
    dy = a[1] - b[1]
    return abs(dx) + abs(dy)


# Input - Ouput
# ---------------
def read_input(stream):
    num_rows, num_cols, num_vehicles, num_rides, bonus, num_steps =\
        list(map(int, stream.readline().split()))
    rides = []
    for i in range(num_rides):
        a, b, x, y, s, f = list(map(int, stream.readline().split()))
        dist = distance((a, b), (x, y))
        latest_start = f - dist - 1
        rides.append(Ride(i, (a, b), (x, y), s, f, latest_start))
    return Config(num_rows, num_cols, num_vehicles, bonus, num_steps), rides


def write(stream, rides_by_vehicle):
    for rides in rides_by_vehicle:
        n_rides = len(rides)
        rides_str = " ".join(map(str, rides))
        stream.write("{} {}\n".format(n_rides, rides_str))


# Scoring
# ---------------
def score_one(current_pos, current_step, ride, config):
    score = 0
    dist_to_start = distance(current_pos, ride.start)
    step_start = max(ride.start_time, current_step + dist_to_start)
    if step_start == ride.start_time:
        score += config.bonus

    dist_start_end = distance(ride.start, ride.finish)
    if step_start + dist_start_end > ride.finish_time:
        return 0, current_step + dist_start_end, ride.finish

    return score + dist_start_end, step_start + dist_start_end, ride.finish


def score(config, rides, rides_by_vehicle):
    total_score = 0
    for v in range(config.num_vehicles):
        current_rides = rides_by_vehicle[v]
        current_step = 0
        current_pos = (0, 0)
        for rid in current_rides:
            ride = rides[rid]
            s, current_step, current_pos = score_one(current_pos, current_step, ride, config)
            total_score += s
    return total_score


# Solver
# ---------------
def rentability(vehicle, ride, config):
    v_available_time = vehicle.step
    dist_pos_to_start = distance(vehicle.pos, ride.start)
    time_v_reach_start = v_available_time + dist_pos_to_start
    if time_v_reach_start > ride.latest_start:
        # can't gain points for the ride
        return -IMPOSSIBLE
    else:
        reward = 0
        if time_v_reach_start <= ride.start_time:
            # get the bonus
            reward += config.bonus
        best_start_time = max(ride.start_time, time_v_reach_start)
        finish_time = best_start_time + distance(ride.start, ride.finish)
        dist_for_client = distance(ride.start, ride.finish)
        reward += dist_for_client + (config.num_steps - finish_time)
        return reward


def update_state(vehicle, ride):
    vehicle.rides.append(ride)
    dstart = distance(vehicle.pos, ride.start)
    time_start = max(ride.start_time, vehicle.step + dstart)
    time_end = time_start + distance(ride.start, ride.finish)
    vehicle.step = time_end
    vehicle.pos = ride.finish


def update_scores(best_vid, scores, vehicles, rides, rides_done, config):
    for rid, r in enumerate(rides):
        if rid not in rides_done:
            scores[(best_vid, rid)] = -rentability(vehicles[best_vid], r, config)


def to_rides_by_vehicles(vehicles):
    rides_by_vehicle = [[] for _ in range(len(vehicles))]
    for vid, v in enumerate(vehicles):
        for r in v.rides:
            rides_by_vehicle[vid].append(r.id)
    return rides_by_vehicle


def solve(config, rides):
    scores = PriorityDict()
    vehicles = [VehicleState((0, 0), 0, []) for _ in range(config.num_vehicles)]
    for vid in range(config.num_vehicles):
        for rid, r in enumerate(rides):
            scores[(vid, rid)] = -rentability(vehicles[vid], r, config)

    rent = 1
    rides_done = set()
    with tqdm(total=config.num_vehicles * len(rides), desc=" processed", unit=" s") as pbar:
        while rent != IMPOSSIBLE:
            (best_vid, best_rid), rent = scores.pop_smallest()
            if best_rid in rides_done:
                continue
            rides_done.add(best_rid)
            update_state(vehicles[best_vid], rides[best_rid])
            update_scores(best_vid, scores, vehicles, rides, rides_done, config)
            pbar.update()

    return to_rides_by_vehicles(vehicles)


if __name__ == "__main__":
    in_filename = sys.argv[1]
    out_filename = sys.argv[2]

    instream = open(in_filename)
    config, rides = read_input(instream)

    outstream = open(out_filename, "w")
    rides_by_vehicle = solve(config, rides)
    write(outstream, rides_by_vehicle)

    s = score(config, rides, rides_by_vehicle)
    print("Score:", s)
