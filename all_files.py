from input import *
import os
import time


if __name__ == "__main__":
    filenames = os.listdir("inputs")
    out_dir = "outputs"
    ts = str(int(time.time()))
    for infilename in filenames:
        infilename = os.path.join("inputs", infilename)
        print("-" * 40)
        print(infilename)
        _, basename = os.path.split(infilename)
        outdirts = os.path.join(out_dir, ts)
        os.makedirs(outdirts, exist_ok=True)
        outfilename = os.path.join(outdirts, basename + ".out")

        instream = open(infilename)
        config, rides = read_input(instream)
        outstream = open(outfilename, "w")

        rides_by_vehicle = solve(config, rides)
        s = score(config, rides, rides_by_vehicle)
        print(f"Score: {s}")

        write(outstream, rides_by_vehicle)