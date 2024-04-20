import csv
import os
import matplotlib.pyplot as plt
import numpy as np


DELTA_T = 3.14*10**(-3)
velocities = [1, 3, 6, 10]


plt.rcParams.update({'font.size': 20})
fig, ax = plt.subplots()
xs = []
ys = []
errors = []

for v in velocities:
    files = [open(os.path.dirname(__file__) + f"/../../total_collisions_{v}_{i}.txt") for i in range(1, 11)]
    slopes = []
    for k in range(len(files)):
        collisions = files[k].readlines()
        for i in range(len(collisions)):
            collisions[i] = int(collisions[i][:-1])
        files[k].close()

        sumXY = 0
        sumX = 0
        sumY = 0
        sumXSquared = 0
        for i in range(len(collisions)):
            sumXY += i * DELTA_T * collisions[i]
            sumX += i * DELTA_T
            sumY += collisions[i]
            sumXSquared += (i * DELTA_T) ** 2

        slope = (len(collisions) * sumXY - sumX * sumY) / (len(collisions) * sumXSquared - sumX ** 2)
        slopes.append(slope)

    xs.append(v * v)
    ys.append(np.average(slopes))
    errors.append(np.std(slopes, ddof=1))

ax.errorbar(xs, ys, yerr=errors, fmt='o', capsize=5, color="tab:blue")

ax.set_xlabel("Temperatura $\\left( U.A. \\right)$", fontdict={"weight": "bold"})
ax.set_ylabel("Número de visitas por unidad de tiempo", fontdict={"weight": "bold"})

# Display the animation
plt.show()
