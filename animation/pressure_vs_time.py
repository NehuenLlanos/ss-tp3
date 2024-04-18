import csv
import matplotlib.pyplot as plt
import numpy as np
import os.path


DELTA_T = 3.14*10**(-3)
WALL_COLLISIONS = ("TOP", "BOTTOM", "LEFT", "RIGHT")


with (open(os.path.dirname(__file__) + '/../output_1_1.txt') as output_file,
      open(os.path.dirname(__file__) + '/../collisions_1_1.txt') as collisions_file,
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

    wall_collisions = {}
    obstacle_collisions = {}
    for i in range(event_count):
        collision_time, collision_object_1, collision_object_2 = float(collisions_data[i][0]), collisions_data[i][2], collisions_data[i][3]

        index = int(collision_time // DELTA_T)
        if index not in wall_collisions:
            wall_collisions[index] = []
        if index not in obstacle_collisions:
            obstacle_collisions[index] = []

        if collision_object_1 in WALL_COLLISIONS or collision_object_2 in WALL_COLLISIONS:
            if collision_object_1 in WALL_COLLISIONS:
                desired_object = collision_object_2
                other_object = collision_object_1
            else:
                desired_object = collision_object_1
                other_object = collision_object_2
            for particle in events[i]:
                if particle[1] == desired_object:
                    wall_collisions[index] = wall_collisions[index] + [(float(particle[4]), float(particle[5]), other_object)]
        elif collision_object_1 == "obstacle" or collision_object_2 == "obstacle":
            desired_object = collision_object_2 if collision_object_1 == "obstacle" else collision_object_1
            for particle in events[i]:
                if particle[1] == desired_object:
                    obstacle_collisions[index] = obstacle_collisions[index] + [(float(particle[4]), float(particle[5]))]

    plt.rcParams.update({'font.size': 20})
    fig, ax = plt.subplots()
    xs = []
    ys = []
    errors = []

    for key in wall_collisions.keys():
        xs.append(key * DELTA_T)
        delta_normal_velocities = []
        for modulus, angle, wall in wall_collisions.get(key):
            if wall == "TOP" or wall == "BOTTOM":
                delta_normal_velocities.append(abs(modulus * np.sin(angle) * 2))
            elif wall == "LEFT" or wall == "RIGHT":
                delta_normal_velocities.append(abs(modulus * np.cos(angle) * 2))

        ys.append(np.sum(delta_normal_velocities) / (DELTA_T * 4 * plane_length))

    line_walls, = ax.plot(xs, ys, linewidth=2.0, label="Presión de paredes")
    ax.set_xlabel("Tiempo  $\\left(s\\right)$", fontdict={"weight": "bold"})
    ax.set_ylabel("Presión  $\\left(Pa\\right)$", fontdict={"weight": "bold"})
    ax.legend(handles=[line_walls])

    # Display the animation
    plt.show()
