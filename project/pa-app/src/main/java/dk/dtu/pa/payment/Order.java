package dk.dtu.pa.payment;
import dk.dtu.pa.Util;


public class Order {

    public Order() {}

    public int calcTotal() {
        OrderDetail od1 = new OrderDetail();
        OrderDetail od2 = new OrderDetail();

        int p1 = od1.price();
        int p2 = od2.price();
        int subSum = Util.sum(p1, p1, p2);

        return Util.sum(subSum, p2);
    }

    public void payOrder() {
        Payment cashPay = new Cash();

        int cashAmount = cashPay.getAmount();
        if (cashAmount > calcTotal() )
        {
            cashPay.pay();
            return;
        }

        Payment creditPay = new Credit();
        int creditAmount = creditPay.getAmount();
        if (creditAmount > calcTotal())
        {
            creditPay.pay();
            return;
        }


    }
}
