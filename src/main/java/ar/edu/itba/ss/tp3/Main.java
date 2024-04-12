package ar.edu.itba.ss.tp3;

import ar.edu.itba.ss.cim.CellIndexMethod;
import ar.edu.itba.ss.cim.Plane;
import ar.edu.itba.ss.tp2.MovingParticle;

import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.List;
import java.util.stream.Stream;

public class Main {
    private static double getRandomAngle() {
        return 2 * Math.PI * Math.random() - Math.PI;
    }

    public static void main(String[] args) {
        List<String> data = null;
        try (Stream<String> stream = Files.lines(Paths.get("input.txt"))) {
            data = stream.toList();
        } catch (Exception e) {
            System.err.println("No input file found");
            System.exit(1);
        }

        if (data.size() != 11) {
            throw new IllegalStateException();
        }

        final int particleCount = Integer.parseInt(data.get(0)); // N
        final double planeLength = Double.parseDouble(data.get(1)); // L
        final double interactionRadius = Double.parseDouble(data.get(2)); // r_c
        final int eventCount = Integer.parseInt(data.get(3)); // N
        final double particleRadius = Double.parseDouble(data.get(4)); // r_particles
        final double particleMass = Double.parseDouble(data.get(5)); // m_particles
        final double particleVelocity = Double.parseDouble(data.get(6)); //v_0_particles
        final double obstacleRadius = Double.parseDouble(data.get(7)); // r_obstacle
        final double obstacleMass = Double.parseDouble(data.get(8)); // m_obstacle
        final double obstacleVelocity = Double.parseDouble(data.get(9)); // v_0_obstacle
        final boolean obstacleMoves = Boolean.parseBoolean(data.get(10)); // obstacle_moves

        Plane.Builder<HeavyMovingParticle> planeBuilder = Plane.Builder.newBuilder();

        HeavyMovingParticle obstacle = HeavyMovingParticle.Builder.newBuilder()
                .withIdentifier("obstacle")
                .withX(planeLength / 2)
                .withY(planeLength / 2)
                .withRadius(obstacleRadius)
                .withMass(obstacleMass)
                .withVelocity(obstacleVelocity)
                .withAngle(getRandomAngle())
                .build();

        List<HeavyMovingParticle> particles = new ArrayList<>();
        particles.add(obstacle);
        for (int i = 0; i < particleCount; i++) {
            HeavyMovingParticle particle = HeavyMovingParticle.Builder.newBuilder()
                    .withIdentifier(String.format("p_%d", i))
                    .withX(0)
                    .withY(0)
                    .withRadius(particleRadius)
                    .withMass(particleMass)
                    .withVelocity(particleVelocity)
                    .withAngle(getRandomAngle())
                    .build();

            do {
                particle.setX(Math.random() * (planeLength - 2 * particleRadius) + particleRadius);
                particle.setY(Math.random() * (planeLength - 2 * particleRadius) + particleRadius);
            } while (particles.stream().anyMatch(p -> p.distanceTo(particle, true) < 0));

            particles.add(particle);
        }
        planeBuilder = planeBuilder.withParticles(particles);

        CellIndexMethod.Builder<HeavyMovingParticle> cimBuilder = CellIndexMethod.Builder.newBuilder();
        final CellIndexMethod<HeavyMovingParticle> cim = cimBuilder
                .withInteractionRadius(interactionRadius)
                .withPlane(planeBuilder.withLength(planeLength).build())
                .build();

        
    }
}
