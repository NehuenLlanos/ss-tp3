import csv
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, FFMpegWriter
import os.path

with(open(os.path.dirname(__file__) + '/../output.txt') as output_file,
    open(os.path.dirname(__file__) + '/../input.txt') as input_file):

    input_data = input_file.readlines()
    particle_count = int(input_data[0][:-1])
    time_count = int(input_data[3][:-1])
    plane_length = float(input_data[1][:-1])

    data = list(csv.reader(output_file, delimiter=" "))

    times = []
    for i in range(time_count):
        times.append(data[i * particle_count:(i + 1) * particle_count])

    fig, ax = plt.subplots()

    def update(i):
        ax.clear()
        ax.set_xlim(0, plane_length)
        ax.set_ylim(0, plane_length)
        ax.grid()
        ax.set_aspect('equal', adjustable='box')

        # Plot each particle
        for particle_data in times[i]:
            x, y = float(particle_data[2]), float(particle_data[3])
            ax.plot(x, y, 'ro')

        return ax

    # Create the animation
    ani = FuncAnimation(fig, update, frames=time_count, blit=False)
    # Display the animation
    # plt.show()
    # Save the animation
    ani.save("../animation.mp4", writer=FFMpegWriter(fps=30))