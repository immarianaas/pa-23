package dk.dtu.pa.persons;

//import java.util.ArrayList;

public class Person {
    private String name;
    private int age;
    private long id;

    private Address address;

    public Person(String name, int age, Address address) {
        this.name = name;
        this.age = age;
        this.address = address;

    }

    public boolean isOlderThan(Person otherPerson) {
        return this.age > otherPerson.age;
    }

    public String getName() {
        return name;
    }

    public Address getAddress() {
        return address;
    }

    public boolean returnBool(Person othPerson) {
        if (this.isOlderThan(othPerson)) {
            return true;
        } else {
            return false;
        }
    }


}
