package dk.dtu.pa;

//import java.util.ArrayList;

import dk.dtu.pa.geometry.*;
import dk.dtu.pa.persons.*;
import dk.dtu.pa.teacher.*;
import dk.dtu.pa.utils.EntryPoint;

/**
 * Hello world!
 *
 */
public class App {
    public static void main(String[] args) {

        // Triangle obj - INTERFACE - ABSTRACT - CLASS - ENUM
        Triangle tr = new Triangle(Type.TRIANGLE, 2, 4);
        System.out.println("Area: " + tr.getArea() + ", Number of sides: " + tr.getNumberOfSides() + tr.getInfo());
        tr.isAreaBigEnough(); 
        tr.returnFalse();

        // Square obj
        Square sq = new Square(Type.SQUARE, 4);
        System.out.println("Area: " + sq.getArea());
        sq.resize(10, 10);

        // Polymorphism with interface
        ResizeShapes sqResizeShape = new Square(Type.SQUARE, 4);
        sqResizeShape.resize(10, 10);






        // Teacher obj - Assistant obj - INTERFACE
        Teacher assistant = new Assistant();
        System.out.println("Subject code: " + String.valueOf(assistant.one_plus_one()));
        assistant.favouriteSubject();
        assistant.classMethod();

        Assistant assistant2 = new Assistant();
        assistant2.isAssistant();
        assistant2.favouriteSubject();





        // Person obj 
        Person person1 = new Person("Alice", 20, new Address());
        Person person2 = new Person("Bob", 15, new Address());

        if (person1.isOlderThan(person2)) {
            System.out.println(person1.getName() + " is older than " + person2.getName());
        } else {
            System.out.println(person2.getName() + " is older than " + person1.getName());
        }



        
        // Persons obj
        Person person3 = new Person("Alice", 20, new Address());
        String address = person3.getAddress()
                .function1("Via Nordvej", person2)
                .function2("2300 ")
                .function3("Kobenhavn")
                .getValue();
        System.out.println("Address is: " + address);
    }

    @EntryPoint
    public void helloWorld() {
        System.out.println("Helloooo");
    }

}
