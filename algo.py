from input import *
from typing import *
import numpy as np

def max_index(a):
    return np.unravel_index(a.argmax(), a.shape)


def algo(config: Config, rides: [Ride]):
    rewards = np.zeros((config.num_vehicles, len(rides)))
    print(rewards.shape)
    vehicles = [VehicleState((0, 0), 0, []) for _ in range(config.num_vehicles)]
    for vid, v in enumerate(vehicles):
        for rid, r in enumerate(rides):
            rewards[vid, rid] = rentability(v, r, config)

    for _ in rides:
        v, r = max_index(rewards)
        update_state(vehicles[v], rides[r])
        update_rewards(rewards, rides, vehicles, v, config)
        rewards[:, r] = -9999

    return to_rides_by_vehicles(vehicles)


def update_rewards(rewards, rides, vehicles, vid, config):
    for rid, r in enumerate(rides):
        rewards[vid, rid] = rentability(vehicles[vid], rides[rid], config)
