package dk.dtu.pa.geometry;


abstract class Shapes implements ResizeShapes {

    protected Type type;
    protected int area;
    protected int perimeter;

    @Override
    public void resize(int base, int high) {
        this.area = base * high;
        this.perimeter = base * 4;
    }

    public abstract int getNumberOfSides();
    public abstract int computeArea(int base, int high);

    public String getInfo(){

        String info = "";
        info = info.concat(String.valueOf(this.area)).concat(String.valueOf(this.perimeter));
        if (this.type == Type.TRIANGLE) {
            info = info.concat(", Shape type: TRIANGLE.");
        } else {
            info = info.concat(", Shape type: SQUARE.");
        }
        return info;
    }




}
