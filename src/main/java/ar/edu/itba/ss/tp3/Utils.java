package ar.edu.itba.ss.tp3;

public class Utils {
    static final double EPSILON = 0.00000001d;

    public static int compare(double a, double b) {
        if (Math.abs(a - b) < EPSILON) {
            return 0;
        } else if (a < b) {
            return -1;
        } else {
            return 1;
        }
    }
}
