package com.example;

public class Main {

    public static void main(String[] args) {
        Main m = new Main();
        System.out.println(m.ret1also());
    }
    
    public int ret1() {
        return 1;
    }

    public int ret1also() {
        return ret1();
    }

    
}