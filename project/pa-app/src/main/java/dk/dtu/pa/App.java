package dk.dtu.pa;

import dk.dtu.pa.geometry.Square;
import dk.dtu.pa.utils.EntryPoint;

/**
 * Hello world!
 *
 */
public class App {
    public static void main(String[] args) {

        Square sq = new Square(5);

        System.out.println("Hello World! Square has perimeter: " + sq.perimeter());
    }

    @EntryPoint
    public int helloWorld() {
        int i = 2;
        int x = i + 1;
        return i + x;
    }

    @EntryPoint
    public double myFirstFunction() {
        Square sq = new Square(2);
        return sq.perimeter();
    }
}
