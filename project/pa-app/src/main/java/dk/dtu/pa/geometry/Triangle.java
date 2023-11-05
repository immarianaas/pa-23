package dk.dtu.pa.geometry;



public class Triangle extends Shapes {
    private final int side = 3;

    public Triangle(Type type, int base, int high) {
        this.type = type;
        this.area = computeArea(base, high);
    }

    public int computeArea(int base, int high) {
        return (base * high) / 2;
    }

    public boolean isAreaBigEnough() {
        if (this.area > this.area + 4) {
            return returnTrue();
        } else {
            return returnFalse();
        }
    }

    public boolean returnTrue() {
        return true;
    }

    public boolean returnFalse() {
        return true;
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
