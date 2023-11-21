package dk.dtu.pa.payment;

public class Credit implements Payment {
    
    public Credit() {}
    
    public int getAmount() {
        return getCreditAmount();
    }

    public int getCreditAmount() {
        return 500;
    }

    public void pay() {
        return; 
    }

}
