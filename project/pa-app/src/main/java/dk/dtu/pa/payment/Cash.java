package dk.dtu.pa.payment;

public class Cash implements Payment {
    
    public Cash() {}
    
    public Cash(int amount) {
        int doubleAmount = amount*2;
    }

    public int getAmount() {
        return getCashAmount();
    }

    public int getCashAmount() {
        return 15;
    }

    public void pay() {
        return; 
    }


}
