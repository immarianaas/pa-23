import math
import os
import json
import glob
import interpreter


def test_alwaysThrows1():
    res = interpreter.interpretMethod(
        "eu/bogoe/dtu/exceptional/Arithmetics", "alwaysThrows1")
    assert (res[1] == {'ArithmeticException - division by 0'})


def test_alwaysThrows2():
    res = interpreter.interpretMethod(
        "eu/bogoe/dtu/exceptional/Arithmetics", "alwaysThrows2", exceptions=[])
    assert (res[1] == {'ArithmeticException - division by 0'})


def test_alwaysThrows3():
    res = interpreter.interpretMethod(
        "eu/bogoe/dtu/exceptional/Arithmetics", "alwaysThrows3", exceptions=[])
    assert (res[1] == {'ArithmeticException - division by 0'})


def test_alwaysThrows4():
    res = interpreter.interpretMethod(
        "eu/bogoe/dtu/exceptional/Arithmetics", "alwaysThrows4", exceptions=[])
    assert (res[1] == {'ArithmeticException - division by 0'})


def test_alwaysThrows5():
    res = interpreter.interpretMethod(
        "eu/bogoe/dtu/exceptional/Arithmetics", "alwaysThrows5", exceptions=[])
    assert (res[1] == {'ArithmeticException - division by 0'})


def test_itDependsOnLattice1():
    res = interpreter.interpretMethod(
        "eu/bogoe/dtu/exceptional/Arithmetics", "itDependsOnLattice1", exceptions=[])
    assert (res[1] == set())


def test_itDependsOnLattice2():
    res = interpreter.interpretMethod(
        "eu/bogoe/dtu/exceptional/Arithmetics", "itDependsOnLattice2", exceptions=[])
    assert (res[1] == set())


def test_itDependsOnLattice3():
    res = interpreter.interpretMethod(
        "eu/bogoe/dtu/exceptional/Arithmetics", "itDependsOnLattice3", exceptions=[])
    assert (res[1] == {'ArithmeticException - division by 0'})  # unsure


def test_itDependsOnLattice4():
    res = interpreter.interpretMethod(
        "eu/bogoe/dtu/exceptional/Arithmetics", "itDependsOnLattice4", exceptions=[])
    assert (res[1] == {'ArithmeticException - division by 0'})

def test_neverThrows1():
    res = interpreter.interpretMethod(
        "eu/bogoe/dtu/exceptional/Arithmetics", "neverThrows1", exceptions=[])
    assert (res[1] == set())

def test_neverThrows2():
    res = interpreter.interpretMethod(
        "eu/bogoe/dtu/exceptional/Arithmetics", "neverThrows2", exceptions=[])
    assert (res[1] == set())

def test_neverThrows3():
    res = interpreter.interpretMethod(
        "eu/bogoe/dtu/exceptional/Arithmetics", "neverThrows3", exceptions=[])
    assert (res[1] == set())

def test_neverThrows4():
    res = interpreter.interpretMethod(
        "eu/bogoe/dtu/exceptional/Arithmetics", "neverThrows4", exceptions=[])
    assert (res[1] == set())

def test_neverThrows5():
    res = interpreter.interpretMethod(
        "eu/bogoe/dtu/exceptional/Arithmetics", "neverThrows5", exceptions=[])
    assert (res[1] == set())


def test_speedVsPrecision():
    res = interpreter.interpretMethod(
        "eu/bogoe/dtu/exceptional/Arithmetics", "speedVsPrecision", exceptions=[])
    assert (res[1] == set())





test_alwaysThrows1()
test_alwaysThrows2()
test_alwaysThrows3()
test_alwaysThrows4()
test_alwaysThrows5()

test_itDependsOnLattice1()
test_itDependsOnLattice2()
test_itDependsOnLattice3()  # TODO: i don't know.. should it throw?
test_itDependsOnLattice4()

test_neverThrows1()

print("\n..neverThrows2.." )
test_neverThrows2()
print()

print("\n..neverThrows3.." )
test_neverThrows3()
print()

print("\n..neverThrows4.." )
test_neverThrows4()
print()

print("\n..neverThrows5.." )
test_neverThrows5()
print()

# test_speedVsPrecision()
# recursion depth problem in our code