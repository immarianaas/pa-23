package dk.dtu.pa.geometry;



public class Triangle extends Shapes {
    private final int side = 3;

    public Triangle(Type type, double base, double high) {
        this.type = type;
        this.area = computeArea(base, high);
        this.perimeter = computePerimeter(base);
    }

    public double computeArea(double base, double high) {
        return (base * high) / 2;
    }

    public double computePerimeter(double base) {
        return base * 3;
    }

    @Override
    public int getNumberOfSides() {
        return this.side;
    }

    public double getArea(){
        return this.area;
    }

    public double getPerimeter() {
        return this.perimeter;
    }

}
