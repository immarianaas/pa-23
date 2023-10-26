package dk.dtu.pa.geometry;


abstract class Shapes implements ResizeShapes {

    protected Type type;
    protected double area;
    protected double perimeter;

    @Override
    public void resize(double base, double high) {
        this.area = base * high;
        this.perimeter = base * 4;
    }

    public abstract int getNumberOfSides();
    public abstract double computeArea(double base, double high);
    public abstract double computePerimeter(double base);

    public String getInfo(){

        String info = "";
        info = info.concat("Area: " + String.valueOf(this.area) + ", Perimeter: " + String.valueOf(this.area) +
        ", Number of sides: " + getNumberOfSides());
        if (this.type == Type.TRIANGLE) {
            info = info.concat(", Shape type: TRIANGLE.");
        } else {
            info = info.concat(", Shape type: SQUARE.");
        }
        return info;
    }




}
