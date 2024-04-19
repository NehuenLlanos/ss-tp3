import csv
import matplotlib.pyplot as plt
import numpy as np
import os.path
import matplotlib.ticker as ticker

DELTA_T = 3.14*10**(-3)

with (open(os.path.dirname(__file__) + '/../output.txt') as output_file,
      open(os.path.dirname(__file__) + '/../collisions.txt') as collisions_file,
      open(os.path.dirname(__file__) + '/../input.txt') as input_file):
    input_data = input_file.readlines()
    particle_count = int(input_data[0][:-1]) + 1
    event_count = int(input_data[3][:-1])
    plane_length = float(input_data[1][:-1])
    particle_radius = float(input_data[4][:-1])
    obstacle_radius = float(input_data[7][:-1])

    events_data = list(csv.reader(output_file, delimiter=" "))
    collisions_data = list(csv.reader(collisions_file, delimiter=" "))

    events = []
    for i in range(event_count):
        events.append(events_data[i * particle_count:(i + 1) * particle_count])

    displacements = {}
    previous_obstacle_x = 0;
    previous_obstacle_y = 0;
    for i in range(event_count):
        collision_time = float(collisions_data[i][0])
        if i == 0:
            previous_obstacle_x = float(events[i][0][2])
            previous_obstacle_y = float(events[i][0][3])
        else:
            index = int(collision_time // DELTA_T)
            if index not in displacements:
                displacements[index] = []

            for particle in events[i]:
                if particle[1] == 'obstacle':
                    current_obstacle_x = float(particle[2])
                    current_obstacle_y = float(particle[3])
                    displacement = np.sqrt((current_obstacle_x - previous_obstacle_x)**2 + (current_obstacle_y - previous_obstacle_y)**2)
                    displacements[index] = displacements[index] + [displacement]
                    previous_obstacle_x = current_obstacle_x
                    previous_obstacle_y = current_obstacle_y

    plt.rcParams.update({'font.size': 20})
    fig, ax = plt.subplots()
    xs = []
    ys = []
    errors = []

    for key in displacements.keys():
        xs.append(key * DELTA_T)
        ys.append(np.sum(displacements.get(key)) / displacements.get(key).__len__())

    ax.plot(xs, ys, linewidth=2.0, label="DCM por DELTA T")
    formatter = ticker.ScalarFormatter()
    formatter.set_scientific(False)
    ax.yaxis.set_major_formatter(formatter)
    ax.set_xlabel("Tiempo [s]", fontdict={"weight": "bold"})
    ax.set_ylabel("Desplazamiento Cuadrático Medio", fontdict={"weight": "bold"})

    # Display the animation
    plt.show()
