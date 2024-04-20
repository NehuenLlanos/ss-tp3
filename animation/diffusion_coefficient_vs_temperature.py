import csv
import os
import matplotlib.pyplot as plt
import numpy as np


with open(os.path.dirname(__file__) + "/../diffusion_coefficient.txt") as file:
    data = list(csv.reader(file, delimiter=" "))
    for i in range(len(data)):
        data[i] = list(map(float, data[i]))

    plt.rcParams.update({'font.size': 20})
    fig, ax = plt.subplots()

    xs = [x[0] ** 2 for x in data]
    ys = [y[1] for y in data]
    errors = [y[2] * 4 for y in data]

    ax.errorbar(xs, ys, yerr=errors, fmt='o', capsize=5)

    ax.set_xlabel("Temperatura $\\left(U.A.\\right)$", fontdict={"weight": "bold"})
    ax.set_ylabel("Coeficiente de difusión $\\left(\\frac{m^2}{s}\\right)$", fontdict={"weight": "bold"})

    # Display the animation
    plt.show()
