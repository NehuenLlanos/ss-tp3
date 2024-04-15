package ar.edu.itba.ss.tp3;

import java.util.Optional;

public class Collision {
    private final HeavyMovingParticle particle1;
    private final HeavyMovingParticle particle2;
    private final boolean withWall;
    private final Wall wall;
    private double time;

    public Collision(HeavyMovingParticle particle1, HeavyMovingParticle particle2, double time) {
        this.particle1 = particle1;
        this.particle2 = particle2;
        this.withWall = false;
        this.wall = null;
        this.time = time;
    }

    public Collision(HeavyMovingParticle particle1, Wall wall, double time) {
        this.particle1 = particle1;
        this.particle2 = null;
        this.withWall = true;
        this.wall = wall;
        this.time = time;
    }

    public HeavyMovingParticle getParticle1() {
        return particle1;
    }

    public HeavyMovingParticle getParticle2() {
        return particle2;
    }

    public boolean isWithWall() {
        return withWall;
    }

    public Wall getWall() {
        return wall;
    }

    public double getTime() {
        return time;
    }

    public void setTime(double time) {
        this.time = time;
    }

    public static Optional<Collision> calculateCollisionWithWall(HeavyMovingParticle particle, Wall wall, double planeLength) {
        final double vx = particle.getVelocity() * Math.cos(particle.getAngle());
        final double vy = particle.getVelocity() * Math.sin(particle.getAngle());
        Double time = null;

        if (wall == Wall.LEFT && Double.compare(vx, 0) < 0) {
            time = (0 + particle.getRadius() - particle.getX()) / vx;
        } else if (wall == Wall.RIGHT && Double.compare(vx, 0) > 0) {
            time = (planeLength - particle.getRadius() - particle.getX()) / vx;
        } else if (wall == Wall.BOTTOM && Double.compare(vy, 0) < 0) {
            time = (0 + particle.getRadius() - particle.getY()) / vy;
        } else if (wall == Wall.TOP && Double.compare(vy, 0) > 0){
            time = (planeLength - particle.getRadius() - particle.getY()) / vy;
        }

        if (time == null) {
            return Optional.empty();
        }
        return Optional.of(new Collision(particle, wall, time));
    }

    public static Optional<Collision> calculateCollisionWithParticle(HeavyMovingParticle particle1, HeavyMovingParticle particle2) {
        final double vx1 = particle1.getVelocity() * Math.cos(particle1.getAngle());
        final double vy1 = particle1.getVelocity() * Math.sin(particle1.getAngle());
        final double vx2 = particle2.getVelocity() * Math.cos(particle2.getAngle());
        final double vy2 = particle2.getVelocity() * Math.sin(particle2.getAngle());
        final double deltaX = particle2.getX() - particle1.getX();
        final double deltaY = particle2.getY() - particle1.getY();
        final double deltaVx = vx2 - vx1;
        final double deltaVy = vy2 - vy1;
        final double sigma = particle1.getRadius() + particle2.getRadius();
        final double d = Math.pow(deltaVx * deltaX + deltaVy * deltaY, 2) - (deltaVx * deltaVx + deltaVy * deltaVy) * (deltaX * deltaX + deltaY * deltaY - sigma * sigma);

        if (deltaVx * deltaX + deltaVy * deltaY >= 0 || d < 0) {
            return Optional.empty();
        }

        final double time = -1 * (deltaVx * deltaX + deltaVy * deltaY + Math.sqrt(d)) / (deltaVx * deltaVx + deltaVy * deltaVy);
        return Optional.of(new Collision(particle1, particle2, time));
    }
}
