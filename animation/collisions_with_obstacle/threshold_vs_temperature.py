import csv
import os
import matplotlib.pyplot as plt
import numpy as np


DELTA_T = 3.14*10**(-3)
PERCENTAGE = 20.0
velocities = [1, 3, 6, 10]


with (open(os.path.dirname(__file__) + "/../../input.txt") as input_file):
    input_data = input_file.readlines()
    particle_count = int(input_data[0][:-1])
    particle_threshold = int(particle_count * PERCENTAGE / 100.0)

    plt.rcParams.update({'font.size': 20})
    fig, ax = plt.subplots()
    xs = []
    ys = []
    errors = []

    for v in velocities:
        files = [open(os.path.dirname(__file__) + f"/../../unique_collisions_{v}_{i}.txt") for i in range(1, 11)]
        times = []
        for k in range(len(files)):
            collisions = files[k].readlines()
            for i in range(len(collisions)):
                collisions[i] = int(collisions[i][:-1])
            files[k].close()

            for i in range(len(collisions)):
                if collisions[i] >= particle_threshold:
                    times.append(i * DELTA_T)
                    break

        xs.append(v * v)
        ys.append(np.average(times))
        errors.append(np.std(times, ddof=1))

    ax.errorbar(xs, ys, yerr=errors, fmt='o', capsize=5, color="tab:blue")

    ax.set_xlabel("Temperatura $\\left( U.A. \\right)$", fontdict={"weight": "bold"})
    ax.set_ylabel(f"Tiempo / {round(PERCENTAGE)}% de partículas chocan c/ obstáculo $\\left(s\\right)$", fontdict={"weight": "bold"})

    # Display the animation
    plt.show()
