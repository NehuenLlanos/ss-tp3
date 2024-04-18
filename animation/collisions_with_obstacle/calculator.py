import csv
import os


DELTA_T = 3.14*10**(-3)


with open(os.path.dirname(__file__) + '/../../collisions.txt') as collisions_file:
    collisions_data = list(csv.reader(collisions_file, delimiter=" "))

    collided_particles = []
    unique_collisions_per_time = {}
    total_collisions_per_time = {}

    for i in range(len(collisions_data)):
        collision_time, collision_object_1, collision_object_2 = float(collisions_data[i][0]), collisions_data[i][2], collisions_data[i][3]
        index = int(collision_time // DELTA_T)
        if index not in unique_collisions_per_time:
            unique_collisions_per_time[index] = 0
        if index not in total_collisions_per_time:
            total_collisions_per_time[index] = 0

        if collision_object_1 == "obstacle" or collision_object_2 == "obstacle":
            desired_object = collision_object_2 if collision_object_1 == "obstacle" else collision_object_1
            if desired_object not in collided_particles:
                collided_particles.append(desired_object)
                unique_collisions_per_time[index] += 1
            total_collisions_per_time[index] += 1

    keys = sorted(unique_collisions_per_time.keys())
    for i in range(len(keys) - 1):
        unique_collisions_per_time[keys[i + 1]] += unique_collisions_per_time[keys[i]]
        total_collisions_per_time[keys[i + 1]] += total_collisions_per_time[keys[i]]

    unique_collisions_output = open(os.path.dirname(__file__) + '/../../unique_collisions.txt', 'w')
    total_collisions_output = open(os.path.dirname(__file__) + '/../../total_collisions.txt', 'w')
    for _, v in sorted(unique_collisions_per_time.items()):
        unique_collisions_output.write(f"{v}\n")
    for _, v in sorted(total_collisions_per_time.items()):
        total_collisions_output.write(f"{v}\n")
    unique_collisions_output.close()
    total_collisions_output.close()
