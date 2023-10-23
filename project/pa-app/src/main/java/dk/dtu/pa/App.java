package dk.dtu.pa;

import dk.dtu.pa.geometry.Square;

/**
 * Hello world!
 *
 */
public class App 
{
    public static void main( String[] args )
    {

        Square sq = new Square(5);

        System.out.println( "Hello World! Square has perimeter: " + sq.perimeter() );
    }
}
