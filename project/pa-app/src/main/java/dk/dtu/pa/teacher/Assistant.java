package dk.dtu.pa.teacher;

public class Assistant implements Teacher {


    public int one_plus_one() {
        return 4;
    }

    public void classMethod() {
        System.out.println("method 2");
    }

    public String favouriteSubject() {
        return "Maths";
    }
}
