import csv
import matplotlib.pyplot as plt
import os.path


RUNS = 10
VEL = 1
EVENT_COUNT = 20000


output_files = [open(os.path.dirname(__file__) + f"/../output_{VEL}_{i}.txt") for i in range(1, RUNS + 1)]
print("Termine")

input_file = open(os.path.dirname(__file__) + '/../input.txt')

input_data = input_file.readlines()
particle_count = int(input_data[0][:-1]) + 1

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

displacements = {}
times = {}
for i in range(RUNS):
    for j in range(EVENT_COUNT):
        if i not in displacements:
            displacements[i] = []
        if i not in times:
            times[i] = []
        displacements[i].append((float(events[i][j][0][2]) - 0.05)**2 + (float(events[i][j][0][3]) - 0.05)**2)
        times[i].append(float(events[i][j][0][0]))

plt.rcParams.update({'font.size': 20})
fig, ax = plt.subplots()
errors = []

for i in range(RUNS):
    ax.plot(times[i], displacements[i], linewidth=2.0)

ax.ticklabel_format(axis="y", style="sci", useMathText=True)
ax.set_xlabel("Tiempo $(s)$", fontdict={"weight": "bold"})
ax.set_ylabel("Desplazamiento Cuadrático $(m^2)$", fontdict={"weight": "bold"})

# Display the animation
plt.show()
