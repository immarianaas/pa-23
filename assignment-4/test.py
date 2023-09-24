import math
import os
import json
import glob
import interpreter


def testNoop():
    res = interpreter.interpretMethod("dtu/compute/exec/Simple", "noop", [])
    assert (res == None)


def testZero():
    res = interpreter.interpretMethod("dtu/compute/exec/Simple", "zero", [])
    assert (res == 0)


def testHundredAndTwo():
    res = interpreter.interpretMethod(
        "dtu/compute/exec/Simple", "hundredAndTwo", [])
    assert (res == 102)


def testIdentity(a):
    res = interpreter.interpretMethod(
        "dtu/compute/exec/Simple", "identity", [a])
    assert (res == a)


def testAdd(a, b):
    res = interpreter.interpretMethod("dtu/compute/exec/Simple", "add", [a, b])
    assert (res == a+b)


def testMin(a, b):
    res = interpreter.interpretMethod("dtu/compute/exec/Simple", "min", [a, b])
    assert (res == min([a, b]))


def testFactorial(n):
    res = interpreter.interpretMethod(
        "dtu/compute/exec/Simple", "factorial", [n])
    assert (res == math.factorial(n))

####################################################################


def testFib(n):
    res = interpreter.interpretMethod("dtu/compute/exec/Calls", "fib", [n])
    def f(n): return 1 if n <= 2 else f(n-1) + f(n-2)
    assert (res == f(n))


def testHelloWorld():
    res = interpreter.interpretMethod(
        "dtu/compute/exec/Calls", "helloWorld", [])

    assert (False)

####################################################################


def testFirst(n):
    res = interpreter.interpretMethod("dtu/compute/exec/Array", "first", [n])
    assert (res == n[0])


def testFirstSafe(n):
    try:
        res = interpreter.interpretMethod(
            "dtu/compute/exec/Array", "firstSafe", [n])
        assert (len(n) > 0 and res == n[0])

    except RuntimeError:
        assert (len(n) == 0)


def testAccess(i, n):
    res = interpreter.interpretMethod(
        "dtu/compute/exec/Array", "access", [i, n])
    assert (res == n[i])


def testNewArray():
    res = interpreter.interpretMethod(
        "dtu/compute/exec/Array", "newArray", [])
    assert (res == 1)


def testNewArrayOutOfBounds():
    try:
        res = interpreter.interpretMethod(
            "dtu/compute/exec/Array", "newArrayOutOfBounds", [])
        assert (False)

    except RuntimeError:
        pass


def testAccessSafe(i, array):
    try:
        res = interpreter.interpretMethod(
            "dtu/compute/exec/Array", "accessSafe", [i, array])
        assert (i >= 0 and i < len(array))
        assert (res == array[i])

    except RuntimeError:
        assert (i < 0 or i >= len(array))


def testBubbleSort(arr):
    temp = arr.copy()
    interpreter.interpretMethod(
        "dtu/compute/exec/Array", "bubbleSort", [arr])

    assert (arr == sorted(temp))


def testAWierdOneOutOfBounds():
    try:
        res = interpreter.interpretMethod(
            "dtu/compute/exec/Array", "aWierdOneOutOfBounds", [])
        assert (False)

    except RuntimeError:
        pass


def testAWierdOneWithinBounds():
    res = interpreter.interpretMethod(
        "dtu/compute/exec/Array", "aWierdOneWithinBounds", [])
    assert (res == 1)

####################################################################

testNoop()
testZero()
testHundredAndTwo()
testIdentity(5)
testAdd(40, 5)
testMin(3, 4)
testFactorial(5)

# testFib(5)
# testHelloWorld()

testFirst([5, 7])
testAccess(1, [5, 7, 8])
testNewArray()
# testBubbleSort( [4, 3, 2, 7] )
testAWierdOneWithinBounds()
testFirstSafe([])
# testAccessSafe(5, [2,3])
testNewArrayOutOfBounds()
testAWierdOneOutOfBounds()

print("Finished running")
