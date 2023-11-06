package com.example;

import com.example.Other.B;
import com.example.Other.C;

public class Test {

    public static int test1() {
        if (Util.identity(1) < Util.identity(2)) {
            return Util.getOne();
        } else {
            return Util.getTwo();
        }

    }

    public static void test2() {
        new B();
    }

    public static int test3() {
        B a = new B();
        return C.baz(a);
    }
}