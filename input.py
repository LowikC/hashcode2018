import sys
from collections import namedtuple
from recordclass import recordclass


Ride = namedtuple("Ride", ["id", "start", "finish", "start_time", "finish_time", "latest_start"])

Config = namedtuple("Config", ["num_rows", "num_cols", "num_vehicles", "bonus", "num_steps"])

VehicleState = recordclass("VehicleState", ["pos", "step", "rides"])


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


def distance(A, B):
    dx = A[0] - B[0]
    dy = A[1] - B[1]
    return abs(dx) + abs(dy)


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


def read_output(stream):
    rides_by_vehicle = []
    for line in stream:
        tokens = list(map(int, line.split()))
        n_rides = tokens[0]
        assert(len(tokens[1:]) == n_rides)
        rides_by_vehicle.append(tokens[1:])
    return rides_by_vehicle


def write(stream, rides_by_vehicle):
    for rides in rides_by_vehicle:
        n_rides = len(rides)
        rides_str = " ".join(map(str, rides))
        stream.write(f"{n_rides} {rides_str}\n")


def find_closest(vehicles, ride):
    min_dist = 1e40
    best_v = None
    for v in vehicles:
        v_available_time = v.step
        # if v.rides:
        #     v_available_time = v.stepv.rides[-1].finish_time
        # else:
        #     v_available_time = 0

        d = distance(v.pos, ride.start)
        if v_available_time + d < ride.latest_start:
            if d < min_dist:
                min_dist = d
                best_v = v
    return best_v


def rentability(vehicle, ride, config):
    if vehicle.rides:
        v_available_time = v.rides[-1].finish_time
    else:
        v_available_time = 0

    time_v_reach_start = v_available_time + distance(vehicle.pos)
    if time_v_reach_start > ride.latest_start:
        # can't gain points for the ride
        return -1
    else:
        reward = 0
        cost = 0
        if time_v_reach_start <= ride.start_time:
            # get the bonus
            reward += config.bonus
            cost += ride.start_time - v_available_time
        else:
            #no bonus
            cost += distance(vehicle.pos, ride.start)
        dist_for_client = distance(ride.start, ride.finish) 
        reward += dist_for_client
        cost += dist_for_client
        return reward / cost

def update_state(vehicle, ride):
    vehicle.rides.append(ride)
    dstart = distance(vehicle.pos, ride.start)
    time_start = max(ride.start_time, vehicle.step + dstart)
    time_end = time_start + distance(ride.start, ride.finish)
    vehicle.step = time_end
    vehicle.pos = ride.finish


def to_rides_by_vehicles(vehicles):
    rides_by_vehicle = [[] for _ in range(len(vehicles))]
    for vid, v in enumerate(vehicles):
        for r in v.rides:
            rides_by_vehicle[vid].append(r.id)
    return rides_by_vehicle


def solve(config, rides):
    rides_by_end_time = sorted(rides, key=lambda x: x.finish_time)
    vehicles = [VehicleState((0, 0), 0, []) for _ in range(config.num_vehicles)]

    for r in rides_by_end_time:
        v = find_closest(vehicles, r)
        if v is not None:
            update_state(v, r)

    return to_rides_by_vehicles(vehicles)



# if __name__ == "__main__":
#     infilename = sys.argv[1]
#     outfilename = sys.argv[2]
#
#     instream = open(infilename)
#     config, rides = read_input(instream)
#
#     outstream = open(outfilename)
#     rides_by_vehicle = read_output(outstream)
#
#     total_score = score(config, rides, rides_by_vehicle)
#     print(f"Score: {total_score}")

if __name__ == "__main__":
    import time
    infilename = sys.argv[1]
    outfilename = infilename + str(int(time.time())) + ".out"

    instream = open(infilename)
    config, rides = read_input(instream)

    outstream = open(outfilename, "w")

    rides_by_vehicle = solve(config, rides)
    s = score(config, rides, rides_by_vehicle)
    print(f"Score: {s}")

    write(outstream, rides_by_vehicle)
