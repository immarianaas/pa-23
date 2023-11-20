package dk.dtu.pa.persons;

public class Address {

    private String value;

    public Address() {
    }

    public Address function1(String str, Person person) {
        String personName = person.getName();
        Person personOld = new Person("Alex", 30, new Address());
        if (person.isOlderThan(personOld)) {
            value = "Sir. " + str;
        } else {
            value = str;
        }
        return this;
    }

    public Address function2(String str) {
        value += " " + str;
        return this;
    }

    public Address function3(String str) {
        value += str;
        return this;
    }

    public String getValue() {
        return value;
    }

}
