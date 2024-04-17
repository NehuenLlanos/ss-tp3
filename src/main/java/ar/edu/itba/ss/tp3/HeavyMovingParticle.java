package ar.edu.itba.ss.tp3;

import ar.edu.itba.ss.tp2.MovingParticle;

public class HeavyMovingParticle extends MovingParticle {
    private double mass;

    protected HeavyMovingParticle(String identifier, double radius, double x, double y, double velocity, double angle, double mass) {
        super(identifier, radius, x, y, velocity, angle);
        this.mass = mass;
    }

    public double getMass() {
        return mass;
    }

    public void setMass(double mass) {
        this.mass = mass;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        if (!super.equals(o)) return false;

        HeavyMovingParticle that = (HeavyMovingParticle) o;

        return Utils.compare(mass, that.mass) == 0;
    }

    @Override
    public int hashCode() {
        int result = super.hashCode();
        long temp;
        temp = Double.doubleToLongBits(mass);
        result = 31 * result + (int) (temp ^ (temp >>> 32));
        return result;
    }

    public static class Builder {
        private String identifier;
        private Double radius;
        private Double x;
        private Double y;
        private Double velocity;
        private Double angle;
        private Double mass;

        protected Builder() {

        }

        public static Builder newBuilder() {
            return new Builder();
        }

        public Builder withIdentifier(String identifier) {
            this.identifier = identifier;
            return this;
        }

        public Builder withRadius(double radius) {
            this.radius = radius;
            return this;
        }

        public Builder withX(double x) {
            this.x = x;
            return this;
        }

        public Builder withY(double y) {
            this.y = y;
            return this;
        }

        public Builder withVelocity(double velocity) {
            this.velocity = velocity;
            return this;
        }

        public Builder withAngle(double angle) {
            this.angle = angle;
            return this;
        }

        public Builder withMass(double mass) {
            this.mass = mass;
            return this;
        }

        public HeavyMovingParticle build() {
            if (this.identifier == null || this.radius == null || this.x == null || this.y == null || this.velocity == null || this.angle == null || this.mass == null) {
                throw new IllegalStateException();
            }
            return new HeavyMovingParticle(
                    this.identifier,
                    this.radius,
                    this.x,
                    this.y,
                    this.velocity,
                    this.angle,
                    this.mass
            );
        }
    }
}
