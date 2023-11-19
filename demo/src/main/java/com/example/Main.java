package com.example;

public class Main {
    public static void main(String[] args) {
        TestConditionals();
        TestOperations();
    }

    public static void TestConditionals() {
        if (Util.identity(1) < Util.identity(2)) {
            Util.A();
        }
        if (Util.identity(-1) > Util.identity(2)) {
            Util.B();
        }
        if (Util.identity(1) < Util.identity(0)) {
            Util.C();
        }
        if (Util.identity(1) != Util.identity(2)) {
            Util.D();
        }
        if (Util.identity(0) != Util.identity(2)) {
            Util.E();
        }
        if (Util.identity(-1) != Util.identity(-2)) {
            Util.F();
        }
        if (Util.identity(-1) != Util.identity(2)) {
            Util.G();
        }
    }

    public static void TestOperations() {
        if (10 + 20 != Util.identity(30)) {
            Util.H();
        }
        if (20 - 10 != Util.identity(10)) {
            Util.I();
        }
        if (-10 * 20 != Util.identity(-200)) {
            Util.J();
        }
        if (-10 + 10 != Util.identity(0)) {
            Util.K();
        }
        if (0 + 10 != Util.identity(10)) {
            Util.L();
        }
        if (10 - -10 != Util.identity(20)) {
            Util.M();
        }
        if (0 * 10 != Util.identity(10)) {
            Util.N();
        }
    }
}