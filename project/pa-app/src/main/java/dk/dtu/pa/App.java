package dk.dtu.pa;

import java.util.ArrayList;

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

        // Triangle obj - INTERFACE - ABSTRACT - ENUM
        Triangle tr = new Triangle(Type.TRIANGLE, 2, 4);
        System.out.println("Area: " + tr.getArea());
        System.out.println("Perimeter: " + tr.getPerimeter());
        System.out.println("Number of sides: " + tr.getNumberOfSides());
        System.out.println(tr.getInfo());
        System.out.println("\r\n");

        // Square obj
        Square sq = new Square(Type.SQUARE, 4);
        System.out.println("Area: " + sq.getArea());
        System.out.println("Perimeter: " + sq.getPerimeter());
        System.out.println("Number of sides: " + sq.getNumberOfSides());
        System.out.println(sq.getInfo());
        sq.resize(10, 10);
        System.out.println("\r\n");

        // Teacher obj - Assistant obj - INTERFACE AND INNER ABSTRACT
        Teacher assistant = new Assistant();

        System.out.println("Subject code: " + String.valueOf(assistant.one_plus_one()));
        assistant.favouriteSubject();
        assistant.classMethod();
        System.out.println("\r\n");

        // Person obj - CONCATENATE METHODS - IF CONDITIONS
        Person person1 = new Person("Alice", 20, new Address());
        Person person2 = new Person("Bob", 15, new Address());

        if (person1.isOlderThan(person2)) {
            System.out.println(person1.getName() + " is older than " + person2.getName());
        } else {
            System.out.println(person2.getName() + " is older than " + person1.getName());
        }

        // Persons obj
        Person person3 = new Person("Alice", 20, new Address());
        ArrayList<String> contacts = person3.setContact();
        String address = person3.getAddress().function1("Via Nordvej", person2).function2("2300 ")
                .function3("Kobenhavn")
                .getValue();
        System.out.println("Address is: " + address);
    }

    @EntryPoint
    public void helloWorld() {
        System.out.println("Helloooo");
    }

}
