package com.example;

import com.example.Other.B;
import com.example.Other.C;
import com.example.Other.D;
import com.example.Other.E;
import com.example.Other.F;

public class Test {

    public Test() {

    }

    public static int test1() {
        if (Util.identity(1) < Util.identity(2)) {
            return Util.getOne();
        } else {
            return Util.getTwo();
        }

    }

    public static void test2() {
        new E();
    }

    public static int test3() {
        F f = new F(5);
        return f.a;
    }

    public static void test4() {
        new B();
    }

    public static int test5() {
        B a = new B();
        return C.baz(a);
    }

    public static int test6() {
        D d = new D(5);
        return d.getA();
    }

    public static int test7() {
        D d = new D(5);
        return d.getA();
    }
}