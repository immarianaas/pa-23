package dk.dtu.pa.geometry;

public class Square {
    private double length;

    public Square( double length ) {
        this.length = length;
    }

    public double perimeter() {
        return length * 4;
    }
}
