package dk.dtu.pa.geometry;

public class Square extends Shapes {
    public final int side = 4;

    public Square(Type type, double side) {
        this.type = type;
        this.area = computeArea (side, side);
        this.perimeter = computePerimeter(side);
    }

    @Override
    public int getNumberOfSides() {
        return this.side;
    }

    public double computeArea(double side, double high) {
        return side * side;
    }

    public double computePerimeter(double side) {
        return side * 4;
    }

    public double getArea(){
        return this.area;
    }

    public double getPerimeter() {
        return this.perimeter;
    }

}
