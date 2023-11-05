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

    public boolean isAssistant() {
        if (one_plus_one() == 2) {
            return false;
        } else {
            return true;
        }
    }
}
