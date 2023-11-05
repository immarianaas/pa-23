package dk.dtu.pa.geometry;

public class Square extends Shapes {
    public final int side = 4;

    public Square(Type type, int side) {
        this.type = type;
        this.area = computeArea (side, side);
    }

    @Override
    public int getNumberOfSides() {
        return this.side;
    }

    public int computeArea(int side, int high) {
        return side * side;
    }


    public boolean hasSide() {
        if (10 < 20) {
            return isSquare();
        } else {
            return isSquare();
        }
    }
    
    private boolean isSquare() {
        if (1 < 2) {
            return true;
        } else {
            return false;
        }
    }

    public int getArea(){
        return this.area;
    }

    public int getPerimeter() {
        return this.perimeter;
    }

}
