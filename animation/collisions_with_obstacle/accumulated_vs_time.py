import csv
import os
import matplotlib.pyplot as plt
import numpy as np


DELTA_T = 1*10**(-3)
FILE = "total"
RUN = 3
VELOCITIES = [1, 3, 6, 10]


plt.rcParams.update({'font.size': 20})
fig, ax = plt.subplots()
lines = []

files = [open(os.path.dirname(__file__) + f'/../../{FILE}_collisions_{v}_3.txt') for v in VELOCITIES]

for file, v in zip(files, VELOCITIES):
    collisions = file.readlines()
    for i in range(len(collisions)):
        collisions[i] = int(collisions[i][:-1])

    xs = np.arange(0, DELTA_T * len(collisions), DELTA_T)
    line, = ax.plot(xs, collisions, linewidth=2.0, label=f"$\\vec{{v}} = {v} \\frac{{m}}{{s}}$")
    lines.append(line)

ax.set_xlabel("Tiempo $\\left(s\\right)$", fontdict={"weight": "bold"})
ax.set_ylabel("Cantidad de colisiones con obstáculo", fontdict={"weight": "bold"})
ax.legend(handles=lines)

# Display the animation
plt.show()
