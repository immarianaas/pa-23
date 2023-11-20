package com.example;

public class Main {
    public static void main(String[] args) {
        TestConditionals();
        TestOperations();
    }

    public static void TestConditionals() {
        if (Util.identity(1) > Util.identity(2)) {
            Util.a();
        }
        if (Util.identity(-1) > Util.identity(2)) {
            Util.b();
        }
        if (Util.identity(1) < Util.identity(0)) {
            Util.c();
        }
        if (Util.identity(1) != Util.identity(2)) {
            Util.d();
        }
        if (Util.identity(0) != Util.identity(2)) {
            Util.e();
        }
        if (Util.identity(-1) != Util.identity(-2)) {
            Util.f();
        }
        if (Util.identity(-1) != Util.identity(2)) {
            Util.g();
        }
    }

    public static void TestOperations() {
        int ten = 10;
        if (ten + 20 != Util.identity(30)) {
            Util.h();
        }
        if (20 - ten != Util.identity(10)) {
            Util.i();
        }
        if (-ten * 20 != Util.identity(-200)) {
            Util.j();
        }
        if (-10 + ten != Util.identity(0)) {
            Util.k();
        }
        if (0 + ten != Util.identity(10)) {
            Util.l();
        }
        if (ten - -10 != Util.identity(20)) {
            Util.m();
        }
        if (0 * ten != Util.identity(10)) {
            Util.n();
        }
    }

    
}