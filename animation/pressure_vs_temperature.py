import csv
import matplotlib.pyplot as plt
import numpy as np
import os.path
import matplotlib.ticker as ticker


DELTA_T = 3.14*10**(-3) * 2
WALL_COLLISIONS = ("TOP", "BOTTOM", "LEFT", "RIGHT")
velocities = [1, 3, 6, 10]
run = 4


with open(os.path.dirname(__file__) + '/../input.txt') as input_file:
    input_data = input_file.readlines()
    particle_count = int(input_data[0][:-1]) + 1
    event_count = int(input_data[3][:-1])
    plane_length = float(input_data[1][:-1])
    particle_radius = float(input_data[4][:-1])
    obstacle_radius = float(input_data[7][:-1])

    events_data_per_velocity = []
    collisions_data_per_velocity = []

    for velocity in velocities:
        collision_file = open(os.path.dirname(__file__) + f'/../collisions_{velocity}_{run}.txt')
        output_file = open(os.path.dirname(__file__) + f'/../output_{velocity}_{run}.txt')
        events_data_per_velocity.append(list(csv.reader(output_file, delimiter=" ")))
        collisions_data_per_velocity.append(list(csv.reader(collision_file, delimiter=" ")))
        collision_file.close()
        output_file.close()

    events_per_velocity = [[] for i in range(len(velocities))]
    for i, events_data in enumerate(events_data_per_velocity):
        for j in range(event_count):
            events_per_velocity[i].append(events_data[j * particle_count:(j + 1) * particle_count])

    wall_collisions_per_velocity = [{} for i in range(len(velocities))]
    obstacle_collisions_per_velocity = [{} for i in range(len(velocities))]

    for v_index, collisions_data in enumerate(collisions_data_per_velocity):
        for i in range(event_count):
            collision_time, collision_object_1, collision_object_2 = float(collisions_data[i][0]), collisions_data[i][2], collisions_data[i][3]

            index = int(collision_time // DELTA_T)
            if index not in wall_collisions_per_velocity[v_index]:
                wall_collisions_per_velocity[v_index][index] = []
            if index not in obstacle_collisions_per_velocity[v_index]:
                obstacle_collisions_per_velocity[v_index][index] = []

            if collision_object_1 in WALL_COLLISIONS or collision_object_2 in WALL_COLLISIONS:
                if collision_object_1 in WALL_COLLISIONS:
                    desired_object = collision_object_2
                    other_object = collision_object_1
                else:
                    desired_object = collision_object_1
                    other_object = collision_object_2
                for particle in events_per_velocity[v_index][i]:
                    if particle[1] == desired_object:
                        wall_collisions_per_velocity[v_index][index] = wall_collisions_per_velocity[v_index][index] + [(float(particle[4]), float(particle[5]), other_object)]
            elif collision_object_1 == "obstacle" or collision_object_2 == "obstacle":
                desired_object = collision_object_2 if collision_object_1 == "obstacle" else collision_object_1
                for particle in events_per_velocity[v_index][i]:
                    if particle[1] == desired_object:
                        obstacle_collisions_per_velocity[v_index][index] = obstacle_collisions_per_velocity[v_index][index] + [(float(particle[2]), float(particle[3]), float(particle[4]), float(particle[5]))]

    wall_pressures_per_velocity = [[] for i in range(len(velocities))]
    obstacle_pressures_per_velocity = [[] for i in range(len(velocities))]

    for v_index, wall_collisions in enumerate(wall_collisions_per_velocity):
        for key in wall_collisions.keys():
            delta_normal_velocities = []
            for modulus, angle, wall in wall_collisions.get(key):
                if wall == "TOP" or wall == "BOTTOM":
                    delta_normal_velocities.append(abs(modulus * np.sin(angle) * 2))
                elif wall == "LEFT" or wall == "RIGHT":
                    delta_normal_velocities.append(abs(modulus * np.cos(angle) * 2))

            wall_pressures_per_velocity[v_index].append(np.sum(delta_normal_velocities) / (DELTA_T * 4 * plane_length))

    for v_index, obstacle_collisions in enumerate(obstacle_collisions_per_velocity):
        for key in obstacle_collisions.keys():
            delta_normal_velocities = []
            for x, y, modulus, angle in obstacle_collisions.get(key):
                alpha = np.arctan2(plane_length / 2 - y, plane_length / 2 - x)
                delta_normal_velocities.append(abs(modulus * np.cos(alpha) * 2))

            obstacle_pressures_per_velocity[v_index].append(np.sum(delta_normal_velocities) / (DELTA_T * 2 * np.pi * obstacle_radius))


    xs = []
    ys_walls = []
    walls_errors = []
    ys_obstacle = []
    obstacle_errors = []

    for v_index, v in enumerate(velocities):
        xs.append(v**2)
        ys_walls.append(np.average(wall_pressures_per_velocity[v_index]))
        walls_errors.append(np.std(wall_pressures_per_velocity[v_index], ddof=1))
        ys_obstacle.append(np.average(obstacle_pressures_per_velocity[v_index]))
        obstacle_errors.append(np.std(obstacle_pressures_per_velocity[v_index], ddof=1))

    plt.rcParams.update({'font.size': 20})
    fig, ax = plt.subplots()


    walls_plot = ax.errorbar(xs, ys_walls, yerr=walls_errors, fmt='o', capsize=5, color="tab:blue", label="Presión de paredes")
    obstacle_plot = ax.errorbar(xs, ys_obstacle, yerr=obstacle_errors, fmt='o', capsize=5, color="tab:orange", label="Presión de obstáculo")

    ax.set_xlabel("Temperatura $\\left(U.A.\\right)$", fontdict={"weight": "bold"})
    ax.set_ylabel("Presión $\\left(Pa \\cdot m\\right)$", fontdict={"weight": "bold"})
    ax.legend(handles=[walls_plot, obstacle_plot])

    ax.ticklabel_format(axis="y", style="sci", useMathText=True)

    plt.show()
