import csv
import os
import matplotlib.pyplot as plt
import numpy as np


DELTA_T = 3.14*10**(-3)
FILE = "unique"

with open(os.path.dirname(__file__) + f'/../../{FILE}_collisions.txt') as collisions_file:
    collisions = collisions_file.readlines()
    for i in range(len(collisions)):
        collisions[i] = int(collisions[i][:-1])

    plt.rcParams.update({'font.size': 20})
    fig, ax = plt.subplots()

    xs = np.arange(0, DELTA_T * len(collisions), DELTA_T)
    print(len(xs), len(collisions))
    ax.plot(xs, collisions, linewidth=2.0)

    ax.set_xlabel("Tiempo (s)", fontdict={"weight": "bold"})
    ax.set_ylabel("Cantidad de colisiones con obstáculo", fontdict={"weight": "bold"})
    # Display the animation
    plt.show()
