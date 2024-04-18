import csv
import matplotlib.pyplot as plt
import numpy as np
import os.path


DELTA_T = 3.14*10**(-3)
WALL_COLLISIONS = ("TOP", "BOTTOM", "LEFT", "RIGHT")


with (open(os.path.dirname(__file__) + '/../output_1ms.txt') as output_file_1ms,
      open(os.path.dirname(__file__) + '/../collisions_1ms.txt') as collisions_file_1ms,
      open(os.path.dirname(__file__) + '/../output_3ms.txt') as output_file_3ms,
      open(os.path.dirname(__file__) + '/../collisions_3ms.txt') as collisions_file_3ms,
      open(os.path.dirname(__file__) + '/../output_6ms.txt') as output_file_6ms,
      open(os.path.dirname(__file__) + '/../collisions_6ms.txt') as collisions_file_6ms,
      open(os.path.dirname(__file__) + '/../output_10ms.txt') as output_file_10ms,
      open(os.path.dirname(__file__) + '/../collisions_10ms.txt') as collisions_file_10ms,
      open(os.path.dirname(__file__) + '/../input.txt') as input_file):
    input_data = input_file.readlines()
    particle_count = int(input_data[0][:-1]) + 1
    event_count = int(input_data[3][:-1])
    plane_length = float(input_data[1][:-1])
    particle_radius = float(input_data[4][:-1])
    obstacle_radius = float(input_data[7][:-1])
    velocity = [1, 3, 6, 10]

    particles_data_per_velocity = {}
    collisions_data_per_velocity = {}

    particles_data_per_velocity[0] = list(csv.reader(output_file_1ms, delimiter=" "))
    collisions_data_per_velocity[0] = list(csv.reader(collisions_file_1ms, delimiter=" "))
    particles_data_per_velocity[1] = list(csv.reader(output_file_3ms, delimiter=" "))
    collisions_data_per_velocity[1] = list(csv.reader(collisions_file_3ms, delimiter=" "))
    particles_data_per_velocity[2] = list(csv.reader(output_file_6ms, delimiter=" "))
    collisions_data_per_velocity[2] = list(csv.reader(collisions_file_6ms, delimiter=" "))
    particles_data_per_velocity[3] = list(csv.reader(output_file_10ms, delimiter=" "))
    collisions_data_per_velocity[3] = list(csv.reader(collisions_file_10ms, delimiter=" "))

    events_per_velocity = {}

    for i in range(len(velocity)):
        events_per_velocity[i] = []

    for i in range(len(velocity)):
        for j in range(event_count):
            events_per_velocity[i].append(particles_data_per_velocity[i][j * particle_count:(j + 1) * particle_count])

    # print(events_per_velocity[0][0])
    wall_collisions_1ms = {}
    wall_collisions_3ms = {}
    wall_collisions_6ms = {}
    wall_collisions_10ms = {}

    for i in range(len(velocity)):
        for j in range(event_count):
            collision_time, collision_object_1, collision_object_2 = float(collisions_data_per_velocity[i][j][0]), collisions_data_per_velocity[i][j][2], collisions_data_per_velocity[i][j][3]
            index = int(collision_time // DELTA_T)
            if i == 0:
                if index not in wall_collisions_1ms:
                    wall_collisions_1ms[index] = []
            if i == 1:
                if index not in wall_collisions_3ms:
                    wall_collisions_3ms[index] = []
            if i == 2:
                if index not in wall_collisions_6ms:
                    wall_collisions_6ms[index] = []
            if i == 3:
                if index not in wall_collisions_10ms:
                    wall_collisions_10ms[index] = []

            if collision_object_1 in WALL_COLLISIONS or collision_object_2 in WALL_COLLISIONS:
                if collision_object_1 in WALL_COLLISIONS:
                    desired_object = collision_object_2
                    other_object = collision_object_1
                else:
                    desired_object = collision_object_1
                    other_object = collision_object_2

                for particle in events_per_velocity[i][j]:
                    if particle[1] == desired_object:
                        if i == 0:
                            wall_collisions_1ms[index] = wall_collisions_1ms[index] + [(float(particle[4]), float(particle[5]), other_object)]
                        if i == 1:
                            wall_collisions_3ms[index] = wall_collisions_3ms[index] + [(float(particle[4]), float(particle[5]), other_object)]
                        if i == 2:
                            wall_collisions_6ms[index] = wall_collisions_6ms[index] + [(float(particle[4]), float(particle[5]), other_object)]
                        if i == 3:
                            wall_collisions_10ms[index] = wall_collisions_10ms[index] + [(float(particle[4]), float(particle[5]), other_object)]

    total_pressure_1ms = 0
    total_pressure_3ms = 0
    total_pressure_6ms = 0
    total_pressure_10ms = 0

    for key in wall_collisions_1ms.keys():
        delta_normal_velocities = []
        for modulus, angle, wall in wall_collisions_1ms.get(key):
            if wall == "TOP" or wall == "BOTTOM":
                delta_normal_velocities.append(abs(modulus * np.sin(angle) * 2))
            elif wall == "LEFT" or wall == "RIGHT":
                delta_normal_velocities.append(abs(modulus * np.cos(angle) * 2))
        total_pressure_1ms += np.sum(delta_normal_velocities) / (DELTA_T * 4 * plane_length)

    for key in wall_collisions_3ms.keys():
        delta_normal_velocities = []
        for modulus, angle, wall in wall_collisions_3ms.get(key):
            if wall == "TOP" or wall == "BOTTOM":
                delta_normal_velocities.append(abs(modulus * np.sin(angle) * 2))
            elif wall == "LEFT" or wall == "RIGHT":
                delta_normal_velocities.append(abs(modulus * np.cos(angle) * 2))
        total_pressure_3ms += np.sum(delta_normal_velocities) / (DELTA_T * 4 * plane_length)

    for key in wall_collisions_6ms.keys():
        delta_normal_velocities = []
        for modulus, angle, wall in wall_collisions_6ms.get(key):
            if wall == "TOP" or wall == "BOTTOM":
                delta_normal_velocities.append(abs(modulus * np.sin(angle) * 2))
            elif wall == "LEFT" or wall == "RIGHT":
                delta_normal_velocities.append(abs(modulus * np.cos(angle) * 2))
        total_pressure_6ms += np.sum(delta_normal_velocities) / (DELTA_T * 4 * plane_length)

    for key in wall_collisions_10ms.keys():
        delta_normal_velocities = []
        for modulus, angle, wall in wall_collisions_10ms.get(key):
            if wall == "TOP" or wall == "BOTTOM":
                delta_normal_velocities.append(abs(modulus * np.sin(angle) * 2))
            elif wall == "LEFT" or wall == "RIGHT":
                delta_normal_velocities.append(abs(modulus * np.cos(angle) * 2))
        total_pressure_10ms += np.sum(delta_normal_velocities) / (DELTA_T * 4 * plane_length)

    average_pressure = []
    average_pressure.append(total_pressure_1ms / len(wall_collisions_1ms.keys()))
    average_pressure.append(total_pressure_3ms / len(wall_collisions_3ms.keys()))
    average_pressure.append(total_pressure_6ms / len(wall_collisions_6ms.keys()))
    average_pressure.append(total_pressure_10ms / len(wall_collisions_10ms.keys()))

    plt.rcParams.update({'font.size': 20})
    fig, ax = plt.subplots()

    for i in range(len(velocity)):
        print(average_pressure[i])
        ax.scatter(velocity[i]**2, average_pressure[i], color='r')

    # 18793.297305781307
    # 168542.2319809217
    # 670360.5433907274
    # 1820482.084769094

    ax.set_xlabel("Temperatura", fontdict={"weight": "bold"})
    ax.set_ylabel("Presión [alguna unidad]", fontdict={"weight": "bold"})


    # Display the animation
    plt.show()
