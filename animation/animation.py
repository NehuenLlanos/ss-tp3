import csv
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.animation import FuncAnimation, FFMpegWriter
import os.path

with (open(os.path.dirname(__file__) + '/../output_1_1.txt') as output_file,
     open(os.path.dirname(__file__) + '/../input.txt') as input_file):
    input_data = input_file.readlines()
    particle_count = int(input_data[0][:-1]) + 1
    time_count = int(input_data[3][:-1])
    plane_length = float(input_data[1][:-1])
    particle_radius = float(input_data[4][:-1])
    obstacle_radius = float(input_data[7][:-1])

    data = list(csv.reader(output_file, delimiter=" "))

    times = []
    for i in range(time_count):
        times.append(data[i * particle_count:(i + 1) * particle_count])

    print("Finished reading data")

    fig, ax = plt.subplots()

    def update(i):
        if i % 1000 == 0:
            print(f"{i} / {time_count}")

        ax.clear()
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)
        ax.set_xlim(0, plane_length)
        ax.set_ylim(0, plane_length)
        ax.set_aspect('equal', adjustable='box')

        # Plot each particle
        for particle_data in times[i]:
            if particle_data[1] == 'obstacle':
                ax.add_patch(
                    mpatches.Circle((float(particle_data[2]), float(particle_data[3])), obstacle_radius, color='b'))
            else:
                ax.add_patch(
                    mpatches.Circle((float(particle_data[2]), float(particle_data[3])), particle_radius, color='r'))
            # ax.annotate(f"{particle_data[1]} - {particle_data[0]}", (float(particle_data[2]), float(particle_data[3])))
        return ax

    print("Starting animation")
    # Create the animation
    ani = FuncAnimation(fig, update, frames=time_count, blit=False, interval=10)

    # Display the animation
    # plt.show()
    print("Starting saving process")
    # Save the animation
    ani.save("../animation.mp4", writer=FFMpegWriter(fps=30))
