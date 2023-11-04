package dk.dtu.pa.geometry;



public class Triangle extends Shapes {
    private final int side = 3;

    public Triangle(Type type, int base, int high) {
        this.type = type;
        this.area = computeArea(base, high);
        this.perimeter = computePerimeter(base);
    }

    public int computeArea(int base, int high) {
        return (base * high) / 2;
    }

    public int computePerimeter(int base) {
        return base * 3;
    }

    @Override
    public int getNumberOfSides() {
        return this.side;
    }

    public int getArea(){
        return this.area;
    }

    public int getPerimeter() {
        return this.perimeter;
    }

}
