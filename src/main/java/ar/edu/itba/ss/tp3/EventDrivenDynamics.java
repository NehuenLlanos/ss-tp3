package ar.edu.itba.ss.tp3;

import ar.edu.itba.ss.cim.CellIndexMethod;

import java.io.BufferedWriter;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.nio.file.StandardOpenOption;
import java.util.*;

public class EventDrivenDynamics {
    private CellIndexMethod<HeavyMovingParticle> cim;
    private HeavyMovingParticle obstacle;
    private boolean obstacleMoves;
    private int eventCount;
    private double elapsedTime = 0;

    public EventDrivenDynamics(CellIndexMethod<HeavyMovingParticle> cim, HeavyMovingParticle obstacle, boolean obstacleMoves, int eventCount) {
        this.cim = cim;
        this.obstacle = obstacle;
        this.obstacleMoves = obstacleMoves;
        this.eventCount = eventCount;
    }

    private void writeResults(String statesFilename, String collisionsFilename, Collision collision) {
        try (
                BufferedWriter statesWriter = Files.newBufferedWriter(
                        Paths.get(statesFilename),
                        StandardOpenOption.APPEND,
                        StandardOpenOption.CREATE
                );
                BufferedWriter collisionsWriter = Files.newBufferedWriter(
                        Paths.get(collisionsFilename),
                        StandardOpenOption.APPEND,
                        StandardOpenOption.CREATE
                )
        ) {
            final ArrayList<HeavyMovingParticle> particles = new ArrayList<>(cim.getPlane().getParticles());
            particles.sort(Comparator.comparing(particle -> particle.getIdentifier().equals("obstacle") ? Integer.MIN_VALUE : Integer.parseInt(particle.getIdentifier().substring(2))));
            for (HeavyMovingParticle particle : particles) {
                statesWriter.write(String.format("%f %s %f %f %f %f", elapsedTime, particle.getIdentifier(), particle.getX(), particle.getY(), particle.getVelocity(), particle.getAngle()));
                statesWriter.newLine();
            }

            if (collision != null) {
                collisionsWriter.write(String.format(
                        "%f %s %s %s",
                        elapsedTime,
                        collision.isWithWall() ? "True" : "False",
                        collision.getParticle1().getIdentifier(),
                        collision.isWithWall() ? collision.getWall() : collision.getParticle2().getIdentifier()));
                collisionsWriter.newLine();
            }
        } catch (IOException e) {
            throw new RuntimeException("Could not write files.");
        }
    }

    public void execute(String statesFilename, String collisionsFilename) {
        try {
            BufferedWriter statesWriter = Files.newBufferedWriter(
                    Paths.get(statesFilename),
                    StandardOpenOption.WRITE,
                    StandardOpenOption.CREATE,
                    StandardOpenOption.TRUNCATE_EXISTING
            );
            BufferedWriter collisionsWriter = Files.newBufferedWriter(
                    Paths.get(collisionsFilename),
                    StandardOpenOption.WRITE,
                    StandardOpenOption.CREATE,
                    StandardOpenOption.TRUNCATE_EXISTING
            );
            statesWriter.close();
            collisionsWriter.close();
        } catch (IOException e) {
            throw new RuntimeException("Could not write files.");
        }

        writeResults(statesFilename, collisionsFilename, null);

        final TreeSet<Collision> collisions = new TreeSet<>(Comparator.comparing(Collision::getTime));

        // Calculate collision with walls
        for (HeavyMovingParticle particle : cim.getPlane().getParticles()) {
            Collision.calculateCollisionWithWall(particle, Wall.LEFT, cim.getPlane().getLength()).ifPresent(collisions::add);
            Collision.calculateCollisionWithWall(particle, Wall.RIGHT, cim.getPlane().getLength()).ifPresent(collisions::add);
            Collision.calculateCollisionWithWall(particle, Wall.BOTTOM, cim.getPlane().getLength()).ifPresent(collisions::add);
            Collision.calculateCollisionWithWall(particle, Wall.TOP, cim.getPlane().getLength()).ifPresent(collisions::add);
        }

        // Calculate collision with other particles
        Map<HeavyMovingParticle, Set<HeavyMovingParticle>> neighbours = cim.execute();
        final Set<HeavyMovingParticle> accountedParticles = new HashSet<>();
        for (Map.Entry<HeavyMovingParticle, Set<HeavyMovingParticle>> entry : neighbours.entrySet()) {
            HeavyMovingParticle particle = entry.getKey();
            accountedParticles.add(particle);
            for (HeavyMovingParticle neighbour : entry.getValue()) {
                if (!accountedParticles.contains(neighbour)) {
                    Collision.calculateCollisionWithParticle(particle, neighbour).ifPresent(collisions::add);
                }
            }
        }

        for (int i = 0; i < eventCount; i++) {
            // Get the first collision
            Collision firstCollision = collisions.pollFirst();
            if (firstCollision == null) {
                throw new IllegalStateException();
            }
            this.elapsedTime += firstCollision.getTime();

            // Move all particles
            for (HeavyMovingParticle particle : cim.getPlane().getParticles()) {
                if (!obstacleMoves && particle.equals(obstacle)) {
                    continue;
                }

                particle.setX(particle.getX() + particle.getVelocity() * Math.cos(particle.getAngle()) * firstCollision.getTime());
                particle.setY(particle.getY() + particle.getVelocity() * Math.sin(particle.getAngle()) * firstCollision.getTime());
            }
            // Update all collisions
            for (Collision collision : collisions) {
                collision.setTime(collision.getTime() - firstCollision.getTime());
            }

            // Write results
            writeResults(statesFilename, collisionsFilename, firstCollision);

            // Update velocities of collided particles
            if (firstCollision.isWithWall()) {
                double newVx, newVy;
                if (firstCollision.getWall() == Wall.LEFT || firstCollision.getWall() == Wall.RIGHT) {
                    newVx = -1 * firstCollision.getParticle1().getVelocity() * Math.cos(firstCollision.getParticle1().getAngle());
                    newVy = firstCollision.getParticle1().getVelocity() * Math.sin(firstCollision.getParticle1().getAngle());
                } else {
                    newVx = firstCollision.getParticle1().getVelocity() * Math.cos(firstCollision.getParticle1().getAngle());
                    newVy = -1 * firstCollision.getParticle1().getVelocity() * Math.sin(firstCollision.getParticle1().getAngle());
                }
                final double newModulus = Math.sqrt(Math.pow(newVx, 2) + Math.pow(newVy, 2));
                final double newAngle = Math.atan2(newVy, newVx);
                firstCollision.getParticle1().setVelocity(newModulus);
                firstCollision.getParticle1().setAngle(newAngle);
            } else {
                final HeavyMovingParticle particle1 = firstCollision.getParticle1();
                final HeavyMovingParticle particle2 = firstCollision.getParticle2();

                final double vx1 = particle1.getVelocity() * Math.cos(particle1.getAngle());
                final double vy1 = particle1.getVelocity() * Math.sin(particle1.getAngle());
                final double vx2 = particle2.getVelocity() * Math.cos(particle2.getAngle());
                final double vy2 = particle2.getVelocity() * Math.sin(particle2.getAngle());
                final double deltaX = particle2.getX() - particle1.getX();
                final double deltaY = particle2.getY() - particle1.getY();
                final double deltaVx = vx2 - vx1;
                final double deltaVy = vy2 - vy1;
                final double sigma = particle1.getRadius() + particle2.getRadius();

                final double j = 2 * particle1.getMass() * particle2.getMass() * (deltaVx * deltaX + deltaVy * deltaY) / (sigma * (particle1.getMass() + particle2.getMass()));
                final double jx = j * deltaX / sigma;
                final double jy = j * deltaY / sigma;

                final double newVx1 = vx1 + jx / particle1.getMass();
                final double newVy1 = vy1 + jy / particle1.getMass();
                final double newVx2 = vx2 - jx / particle2.getMass();
                final double newVy2 = vy2 - jy / particle2.getMass();

                final double newModulus1 = Math.sqrt(Math.pow(newVx1, 2) + Math.pow(newVy1, 2));
                final double newAngle1 = Math.atan2(newVy1, newVx1);
                final double newModulus2 = Math.sqrt(Math.pow(newVx2, 2) + Math.pow(newVy2, 2));
                final double newAngle2 = Math.atan2(newVy2, newVx2);

                particle1.setVelocity(newModulus1);
                particle1.setAngle(newAngle1);
                particle2.setVelocity(newModulus2);
                particle2.setAngle(newAngle2);
            }

            // Update collisions
            collisions.removeIf(collision -> {
                if (collision.isWithWall()) {
                    return collision.getParticle1().equals(firstCollision.getParticle1()) || collision.getParticle1().equals(firstCollision.getParticle2());
                } else {
                    return collision.getParticle1().equals(firstCollision.getParticle1()) ||
                            collision.getParticle1().equals(firstCollision.getParticle2()) ||
                            (collision.getParticle2() != null && collision.getParticle2().equals(firstCollision.getParticle1())) ||
                            (collision.getParticle2() != null && collision.getParticle2().equals(firstCollision.getParticle2()));
                }
            });

            neighbours = cim.execute();
            if (firstCollision.getParticle1() != null) {
                Collision.calculateCollisionWithWall(firstCollision.getParticle1(), Wall.LEFT, cim.getPlane().getLength()).ifPresent(collisions::add);
                Collision.calculateCollisionWithWall(firstCollision.getParticle1(), Wall.RIGHT, cim.getPlane().getLength()).ifPresent(collisions::add);
                Collision.calculateCollisionWithWall(firstCollision.getParticle1(), Wall.BOTTOM, cim.getPlane().getLength()).ifPresent(collisions::add);
                Collision.calculateCollisionWithWall(firstCollision.getParticle1(), Wall.TOP, cim.getPlane().getLength()).ifPresent(collisions::add);

                for (HeavyMovingParticle neighbour : neighbours.get(firstCollision.getParticle1())) {
                    Collision.calculateCollisionWithParticle(firstCollision.getParticle1(), neighbour).ifPresent(collisions::add);
                }
            }
            if (firstCollision.getParticle2() != null) {
                Collision.calculateCollisionWithWall(firstCollision.getParticle2(), Wall.LEFT, cim.getPlane().getLength()).ifPresent(collisions::add);
                Collision.calculateCollisionWithWall(firstCollision.getParticle2(), Wall.RIGHT, cim.getPlane().getLength()).ifPresent(collisions::add);
                Collision.calculateCollisionWithWall(firstCollision.getParticle2(), Wall.BOTTOM, cim.getPlane().getLength()).ifPresent(collisions::add);
                Collision.calculateCollisionWithWall(firstCollision.getParticle2(), Wall.TOP, cim.getPlane().getLength()).ifPresent(collisions::add);

                for (HeavyMovingParticle neighbour : neighbours.get(firstCollision.getParticle2())) {
                    if (!neighbour.equals(firstCollision.getParticle1())) {
                        Collision.calculateCollisionWithParticle(firstCollision.getParticle2(), neighbour).ifPresent(collisions::add);
                    }
                }
            }
        }
    }

    public static class Builder {
        private CellIndexMethod<HeavyMovingParticle> cim;
        private HeavyMovingParticle obstacle;
        private Boolean obstacleMoves;
        private Integer eventCount;

        protected Builder() {

        }

        public static Builder newBuilder() {
            return new Builder();
        }

        public Builder withCim(CellIndexMethod<HeavyMovingParticle> cim) {
            this.cim = cim;
            return this;
        }

        public Builder withObstacle(HeavyMovingParticle obstacle) {
            this.obstacle = obstacle;
            return this;
        }

        public Builder withMovingObstacle(boolean obstacleMoves) {
            this.obstacleMoves = obstacleMoves;
            return this;
        }

        public Builder withEventCount(int eventCount) {
            this.eventCount = eventCount;
            return this;
        }

        public EventDrivenDynamics build() {
            if (cim == null || obstacle == null || obstacleMoves == null || eventCount == null) {
                throw new IllegalStateException();
            }

            return new EventDrivenDynamics(
                    cim,
                    obstacle,
                    obstacleMoves,
                    eventCount
            );
        }
    }
}
