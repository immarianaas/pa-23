package dk.dtu.pa.geometry;

public class Square extends Shapes {
    public final int side = 4;

    public Square(Type type, int side) {
        this.type = type;
        this.area = computeArea (side, side);
        this.perimeter = computePerimeter(side);
    }

    @Override
    public int getNumberOfSides() {
        return this.side;
    }

    public int computeArea(int side, int high) {
        return side * side;
    }

    public int computePerimeter(int side) {
        return side * 4;
    }

    public int getArea(){
        return this.area;
    }

    public int getPerimeter() {
        return this.perimeter;
    }

}
