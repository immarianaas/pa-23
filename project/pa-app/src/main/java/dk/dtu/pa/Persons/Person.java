package dk.dtu.pa.Persons;

import java.util.ArrayList;
import java.util.List;

public class Person {
    private String name;
    private int age;

    private long Id;

    private Address address;
    private ArrayList<String> contact;


    public Person(String name, int age, Address address) {
        this.name = name;
        this.age = age;
        this.address = address;
        this.contact = new ArrayList();

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

    public ArrayList<String> setContact() {
        var listInfo= new ArrayList<String>();
        listInfo.add("Name");
        listInfo.add("Address");
        this.contact = listInfo;
        return listInfo;
    }

}
