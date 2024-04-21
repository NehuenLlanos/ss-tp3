# Evemt Driven Simulation: Molecular Dynamics of Hard Spheres

## Introduction

This project simulates the molecular dynamics of hard spheres. The particles are located in a square plane and interact with each other when they are within a certain radius. The collisions between particles and the walls are elastic. The evolution of this system is studied to analyze if the particles behave like an ideal gas. 

## Requirements

* Java 19
* Maven
* Python 3 (only if you want the visualizations to be rendered)

## Building the project

To build the project, `cd` to the root of the project and run the following command:

```bash
mvn clean package
```

This will compile and package a `.jar` file in the `target` directory.

## Executing the project

> [!NOTE]  
> The following instructions assume that you have built the project as described in the previous section and that the generated `.jar` file is in the current working directory.

The program expects to have an input file named `input.txt` in the current working directory. The input file should contain the following structure:

```text
{{ number_of_particles }}
{{ plane_length }}
{{ interaction_radius }}
{{ epochs }}
{{ particle_radius }}
{{ particle_mass }}
{{ particle_initial_velocity }}
{{ obstacle_radius }}
{{ obstacle_mass }}
{{ obstacle_initial_velocity }}
{{ obstacle_moves }}
```

Where:

* `number_of_particles` is the number of particles in the simulation. Must be an integer.
* `plane_length` is the length of the square plane where the particles are located. Must be a floating point number.
* `interaction_radius` is the radius of the interaction between particles. Must be a floating point number. For the simulation to work perfectly, must be equal to the plane length.
* `epochs` is the number of events the simulation will run for. Must be an integer.
* `particle_radius` is the radius of the particles. Must be a floating point number.
* `particle_mass` is the mass of the particles. Must be a floating point number.
* `particle_initial_velocity` is the initial velocity of the particles. Must be a floating point number.
* `obstacle_radius` is the radius of the obstacle. Must be a floating point number.
* `obstacle_mass` is the mass of the obstacle. Must be a floating point number.
* `obstacle_initial_velocity` is the initial velocity of the obstacle. Must be a floating point number.
* `obstacle_moves` is a boolean value indicating if the obstacle moves. Must be `true` or `false`.

To execute the project, run the following command:

```bash
java -jar ss-tp3-1.0-SNAPSHOT.jar
```

This will execute the program and generate a series of output files named `output_{{ velocity }}_{{ run }}.txt` and `collisions_{{ velocity }}_{{ run }}.txt` in the current working directory. The simulation will run for each velocity value in ${1, 3, 6, 10}$, ten times for each velocity value.

The output file will have the following structure:

```text
{{ time }} {{ particle_id }} {{ x_position }} {{ y_position }} {{ velocity_module }} {{ velocity_angle }}
...
```

Where:

* `time` is the current time of the simulation.
* `particle_id` is the identifier of the particle.
* `x_position` is the x-coordinate of the particle on that step.
* `y_position` is the y-coordinate of the particle on that step.
* `velocity_module` is the module of the velocity of the particle on that step.
* `velocity_angle` is the angle of the velocity of the particle on that step.

There will be one line for each particle and event in the simulation. For example: if there are 300 particles and the simulation runs for 100 events, the file will have 30000 lines.

The collisions file will have the following structure:

```text
{{ time }} {{ collision_with_wall }} {{ collision_object_1 }} {{ collision_object_2 }}
```

Where:

* `time` is the current time of the simulation.
* `collision_with_wall` is a boolean value indicating if the collision was with a wall. Will be `true` or `false`.
* `collision_object_1` is the identifier of the first object involved in the collision.
* `collision_object_2` is the identifier of the second object involved in the collision. If the collision was with a wall, then the value will be `TOP`, `BOTTOM`, `LEFT` or `RIGHT`, indicating which wall was collided.

## Visualizing the output

> [!NOTE]  
> The following instructions assume that you have executed the project as described in the previous section and that the files `input.txt`, `output_{{ velocity }}_{{ run }}.txt` and `collisions_{{ velocity }}_{{ run }}.txt` are in the current working directory.

### Installing dependencies

To visualize the output, we must run a series of Python scripts. First, we need to install the required dependencies. To do so, run the following command:

```bash
python -m venv venv
source venv/bin/activate
pip install -r animation/requirements.txt
```

### Generating the animation

You must specify which output file you want to visualize. To do so, edit the `animation/animation.py` file and change the name of the output file to the desired one.

To visualize an animation of the simulation, run the following command:

```bash
python animation/animation.py
```

This will generate an animation of the particles in the simulation. You will be able to see how the particles move and how they collide with each other and the walls.

### Visualizing the pressure vs time graph

The pressure of the system is a measure of how excited the particles are. To visualize the pressure vs time graph, run the following command:

```bash
python animation/pressure_vs_time.py
```

This will generate a graph showing the pressure of the walls and obstacle over time.

### Visualizing the pressure vs temperature graph

The pressure of the system is expected to increase as we increase the system's temperature. To visualize the pressure vs temperature graph, run the following command:

```bash
python animation/pressure_vs_temperature.py
```

### Visualizing the square displacement of the obstacle vs time graph

The square displacement of the obstacle is a measure of how much the obstacle moves. To visualize the square displacement of the obstacle vs time graph, run the following command:

```bash
python animation/dc_vs_time.py
```

This will generate a graph showing the square displacement of the obstacle over time, for all of the runs that were made.

### Visualizing the mean square displacement of the obstacle vs time graph

The mean square displacement of the obstacle is a measure of how much the obstacle moves on average. To visualize the mean square displacement of the obstacle vs time graph, run the following command:

```bash
python animation/dcm_vs_time.py
```

This will generate a graph showing the mean square displacement of the obstacle over time, for all the velocities.

### Visualizing the diffusion coefficient vs temperature graph

The diffusion coefficient is a measure of how much the particles move. It is calculated as the slope of the linear dependency between the mean square displacement of the particles and the time, divided by four. 

To visualize the diffusion coefficient vs temperature graph, run the following command:

```bash
python animation/diffusion_coefficient_vs_temperature.py
```

### Collisions of particles to the obstacle

It is also interesting to analyze how many particles collide with the obstacle, and how this varies with the particle's initial velocity.

#### Generating the data

To generate the data, run the following command:

```bash
python animation/collisions_with_obstacle/calculator.py
```

This will generate a series of output files named `unique_collisions_{{ velocity }}_{{ run }}.txt` and `total_collisions_{{ velocity }}_{{ run }}.txt`. For each file, the corresponding `colliions_{{ velocity }}_{{ run }}.txt` will be used. The output files will have the following structure:

```text
{{ accumulated_collisions_t0 }}
{{ accumulated_collisions_t1 }}
...
```

The `unique_collisions_{{ velocity }}_{{ run }}.txt` file will have the accumulated number of unique particles that collided with the obstacle at each time step. The `total_collisions_{{ velocity }}_{{ run }}.txt` file will have the accumulated number of total collisions with the obstacle at each time step.

#### Visualizing the accumulated collisions vs time graph

You must specify the index of the run you want to visualize. To do so, edit the `animation/collisions_with_obstacle/accumulated_vs_time.py` file and change the value of the `RUN` variable to the desired index.

To visualize the accumulated collisions vs time graph, run the following command:

```bash
python animation/collisions_with_obstacle/accumulated_vs_time.py
```

#### Visualizing the observable value vs temperature graph

The observable value will change whether we want to analyze unique or total collisions.:

* If we analyze unique collisions, the observable value is the time until a percentage of the particles have collided with the obstacle.
* If we analyze total collisions, the observable value is the number of collisions per unit of time.

To visualize the collision threshold vs temperature graph, run the following command:

```bash
python animation/collisions_with_obstacle/threshold_vs_temperature.py
```

To visualize the collision per unit of time vs temperature graph, run the following command:

```bash
python animation/collisions_with_obstacle/slope_vs_temperature.py
```

## Final Remarks

This project was done in an academic environment, as part of the curriculum of Systems Simulation from Instituto Tecnológico de Buenos Aires (ITBA)

The project was carried out by:

* Alejo Flores Lucey
* Nehuén Gabriel Llanos