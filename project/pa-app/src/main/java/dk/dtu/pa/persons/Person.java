package dk.dtu.pa.persons;

//import java.util.ArrayList;

public class Person {
    private String name;
    private int age;

    private long id;

    private Address address;
//    private ArrayList<String> contact;

    public Person(String name, int age, Address address) {
        this.name = name;
        this.age = age;
        this.address = address;
//        this.contact = new ArrayList<String>();
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

//    public ArrayList<String> setContact() {
//        ArrayList<String> listInfo = new ArrayList<String>();
//        listInfo.add("Name");
//        listInfo.add("Address");
//        this.contact = listInfo;
//        return listInfo;
//    }

}
