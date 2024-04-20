import csv
import matplotlib.pyplot as plt
import os.path
import numpy as np


def best_slope(xs, ys):
    Y_INTERCEPT = 0
    LINEAR_FUNCTION = lambda x, m: m * x + Y_INTERCEPT
    TRIES = 30

    candidate_slope = 0
    min_error = np.inf

    max_slope = max(ys) / max(xs)
    slopes = np.arange(0, max_slope, max_slope / TRIES)

    for slope in slopes:
        error = 0
        for x, y in zip(xs, ys):
            error += (y - LINEAR_FUNCTION(x, slope))**2
        if error < min_error:
            min_error = error
            candidate_slope = slope

    return candidate_slope, min_error


RUNS = 10
VELOCITIES = [1, 3, 6, 10]
EVENT_COUNT = 20000
TIME_LIMITS = [0.065, 0.035, 0.021, 0.015]
DELTA_TS = [0.00065, 0.00035, 0.00021, 0.00015]
COLORS = [("tab:blue", "lightsteelblue"), ("tab:orange", "navajowhite"), ("tab:green", "lightgreen"), ("tab:red", "lightcoral")]


plt.rcParams.update({'font.size': 20})
fig, ax = plt.subplots()
labels = []
diffusion_coefficient_file = open(os.path.dirname(__file__) + f"/../diffusion_coefficient.txt", 'w')

for VEL, TIME_LIMIT, DELTA_T, COLOR in zip(VELOCITIES, TIME_LIMITS, DELTA_TS, COLORS):
    INTERVAL_COUNT = round(TIME_LIMIT / DELTA_T)
    print(VEL, TIME_LIMIT, DELTA_T, INTERVAL_COUNT)

    output_files = [open(os.path.dirname(__file__) + f"/../output_{VEL}_{i}.txt") for i in range(1, RUNS + 1)]
    print("Termine")

    input_file = open(os.path.dirname(__file__) + '/../input.txt')
    input_data = input_file.readlines()
    particle_count = int(input_data[0][:-1]) + 1
    plane_length = float(input_data[1][:-1])

    events_data = {}
    for i in range(RUNS):
        if i not in events_data:
            events_data[i] = []
        events_data[i] = list(csv.reader(output_files[i], delimiter=" "))

    print("Termine de leer los archivos")
    for file in output_files:
        file.close()

    events = {}
    for i in range(RUNS):
        for j in range(EVENT_COUNT):
            if i not in events:
                events[i] = []
            events[i].append(events_data[i][j * particle_count:(j + 1) * particle_count])

    print("Termine de leer los eventos")

    # Diccionario que tiene como key a cada corrida y como value a un objeto formado por el desplzamiento para un tiempo
    # determinado y el tiempo en el que se dio dicho desplazamiento
    displacements = {}
    for i in range(RUNS):
        for j in range(EVENT_COUNT):
            if i not in displacements:
                displacements[i] = []
            displacements[i].append([(float(events[i][j][0][2]) - plane_length / 2)**2 + (float(events[i][j][0][3]) - plane_length / 2)**2, float(events[i][j][0][0])])

    displacements_normalized = {}
    for i in range(RUNS):
        previous_index = 0
        displacements_normalized[i] = []
        displacements_normalized[i].append(displacements[i][0][0])
        j = 1
        while displacements[i][j][1] < TIME_LIMIT:
            current_index = int(displacements[i][j][1] // DELTA_T)
            if previous_index < current_index:
                displacements_normalized[i].append(displacements[i][j][0])
            previous_index = current_index
            j += 1

    xs = [DELTA_T * i for i in range(INTERVAL_COUNT)]
    dcm = [0 for _ in range(INTERVAL_COUNT)]
    for i in range(INTERVAL_COUNT):
        dcm[i] = [displacements_normalized[x][i] for x in range(RUNS)]

    for i in range(INTERVAL_COUNT):
        dcm[i] = np.average(dcm[i])

    slope, error = best_slope(xs, dcm)
    ys = [slope * x for x in xs]
    diffusion_coefficient_file.write(f"{VEL} {slope / 4} {error / 4}\n")

    ax.plot(xs, ys, color=COLOR[1], linewidth=2.0)
    line = ax.errorbar(xs, dcm, yerr=None, fmt='o', capsize=5, color=COLOR[0], label=f"$\\vec{{v}} = {VEL} \\frac{{m}}{{s}}$")
    labels.append(line)

diffusion_coefficient_file.close()
ax.ticklabel_format(axis="y", style="sci", useMathText=True)
ax.set_xlabel("Tiempo $(s)$", fontdict={"weight": "bold"})
ax.set_ylabel("Desplazamiento Cuadrático Medio $(m)$", fontdict={"weight": "bold"})
ax.legend(handles=labels)

# Display the animation
plt.show()
