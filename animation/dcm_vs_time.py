import csv
import matplotlib.pyplot as plt
import os.path
import numpy as np
import matplotlib.ticker as ticker

RUNS = 3
VEL = 1
EVENT_COUNT = 4847
DELTA_T = 0.0015
output_files = {}

output_files[0] = open(os.path.dirname(__file__) + '/../output_1ms_run1.txt')
output_files[1] = open(os.path.dirname(__file__) + '/../output_1ms_run2.txt')
output_files[2] = open(os.path.dirname(__file__) + '/../output_1ms_run3.txt')
output_files[3] = open(os.path.dirname(__file__) + '/../output_1ms_run4.txt')
output_files[4] = open(os.path.dirname(__file__) + '/../output_1ms_run5.txt')
# output_files[5] = open(os.path.dirname(__file__) + '/../output_1ms_run6.txt')
# output_files[6] = open(os.path.dirname(__file__) + '/../output_1ms_run7.txt')
# output_files[7] = open(os.path.dirname(__file__) + '/../output_1ms_run8.txt')
# output_files[8] = open(os.path.dirname(__file__) + '/../output_1ms_run9.txt')
# output_files[9] = open(os.path.dirname(__file__) + '/../output_1ms_run10.txt')
# output_files[10] = open(os.path.dirname(__file__) + '/../output_1ms_run11.txt')
print("Termine")

input_file = open(os.path.dirname(__file__) + '/../input.txt')

input_data = input_file.readlines()
particle_count = int(input_data[0][:-1]) + 1
event_count = int(input_data[3][:-1])
plane_length = float(input_data[1][:-1])
particle_radius = float(input_data[4][:-1])
obstacle_radius = float(input_data[7][:-1])

events_data = {}
for i in range(RUNS):
    if i not in events_data:
        events_data[i] = []
    events_data[i] = list(csv.reader(output_files[i], delimiter=" "))

print("Termine de leer los archivos")

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
        displacements[i].append([(float(events[i][j][0][2]) - 0.05)**2 + (float(events[i][j][0][3]) - 0.05)**2, float(events[i][j][0][0])])

plt.rcParams.update({'font.size': 20})
fig, ax = plt.subplots()
errors = []


displacements_normalized = {}
for i in range(RUNS):
    previous_index = 0
    displacements_normalized[i] = []
    displacements_normalized[i].append(displacements[i][0][0])
    j = 1
    while displacements[i][j][1] < 0.15:
        current_index = int(displacements[i][j][1] // DELTA_T)
        if previous_index < current_index:
            displacements_normalized[i].append(displacements[i][j][0])
        previous_index = current_index

xs = np.arange(0, 0.15, DELTA_T)
dcm = [0 for in range(100)]
for i in range(100):
    dcm[i] = [displacements_normalized[x][i] for x in range(RUNS)]

for i in range(100):
    dcm[i] = np.average(dcm[i])

ax.plot(xs, dcm, linewidth=2.0)

formatter = ticker.ScalarFormatter()
formatter.set_scientific(False)
ax.yaxis.set_major_formatter(formatter)
ax.set_xlabel("Tiempo $(s)$", fontdict={"weight": "bold"})
ax.set_ylabel("Desplazamiento Cuadrático Medio $(m)$", fontdict={"weight": "bold"})

# Display the animation
plt.show()
