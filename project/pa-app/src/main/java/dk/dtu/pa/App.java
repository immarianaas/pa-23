package dk.dtu.pa;

import dk.dtu.pa.geometry.*;
import dk.dtu.pa.Teacher.*;
import dk.dtu.pa.Persons.*;

import dk.dtu.pa.utils.EntryPoint;

import java.util.ArrayList;

/**
 * Main function as entry point
 *
 */
public class App {
    @EntryPoint
    public static void main(String[] args) {

        // Triangle obj - INTERFACE - ABSTRACT - ENUM
        var tr = new Triangle(Type.TRIANGLE, 2, 4);
        System.out.println("Area: " + tr.getArea());
        System.out.println("Perimeter: " + tr.getPerimeter());
        System.out.println("Number of sides: " + tr.getNumberOfSides());
        System.out.println(tr.getInfo());
        System.out.println("\r\n");

        //Square obj
        Square sq = new Square(Type.SQUARE, 4);
        System.out.println("Area: " + sq.getArea());
        System.out.println("Perimeter: " + sq.getPerimeter());
        System.out.println("Number of sides: " + sq.getNumberOfSides());
        System.out.println(sq.getInfo());
        sq.resize(10, 10);
        System.out.println("\r\n");


        // Teacher obj - Assistant obj - INTERFACE AND INNER ABSTRACT
        var assistant = new Assistant();
        Teacher.Subject teacher = new Teacher.Subject(2) {
            public String favouriteSubject() { return "History"; }
        };
        System.out.println("Subject code: " + teacher.getSubjectCode());
        teacher.favouriteSubject();
        assistant.ClassMethod();
        System.out.println("\r\n");


        // Person obj - CONCATENATE METHODS - IF CONDITIONS
        var person1 = new Person("Alice", 20, new Address());
        var person2 = new Person("Bob", 15, new Address());

        if (person1.isOlderThan(person2)) {
            System.out.println(person1.getName() + " is older than " + person2.getName());
        } else {
            System.out.println(person2.getName() + " is older than " + person1.getName());
        }

        // Persons obj
        var person3 = new Person("Alice", 20, new Address());
        var contacts = person3.setContact();
        var address = person3.getAddress().function1("Via Nordvej", person2).function2("2300 ").function3("Kobenhavn").getValue();
        System.out.println("Address is: " + address);
    }

}
