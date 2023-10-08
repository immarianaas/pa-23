import os
import interpreter


interpreter.interpretProjDir(os.path.join(".",
                 "course-02242-examples", "decompiled"))


res = interpreter.interpretMethod(
    "eu/bogoe/dtu/exceptional/Arithmetics", "alwaysThrows1")
assert(interpreter.Exception.ArithmeticException in [e for (_,e) in sum(res,[]) ])

res = interpreter.interpretMethod(
    "eu/bogoe/dtu/exceptional/Arithmetics", "alwaysThrows2")
assert(interpreter.Exception.ArithmeticException in [e for (_,e) in sum(res,[]) ])


res = interpreter.interpretMethod(
    "eu/bogoe/dtu/exceptional/Arithmetics", "alwaysThrows3")
assert(interpreter.Exception.ArithmeticException in [e for (_,e) in sum(res,[]) ])

# this is the first that uses assert.....
# assert is not really implemented yet, though..
res = interpreter.interpretMethod(
    "eu/bogoe/dtu/exceptional/Arithmetics", "alwaysThrows4")
assert(interpreter.Exception.ArithmeticException in [e for (_,e) in sum(res,[]) ])

res = interpreter.interpretMethod(
    "eu/bogoe/dtu/exceptional/Arithmetics", "alwaysThrows5")
print(res)

res = interpreter.interpretMethod(
    "eu/bogoe/dtu/exceptional/Arithmetics", "itDependsOnLattice1")
print(res)

res = interpreter.interpretMethod(
    "eu/bogoe/dtu/exceptional/Arithmetics", "itDependsOnLattice2")

res = interpreter.interpretMethod(
    "eu/bogoe/dtu/exceptional/Arithmetics", "itDependsOnLattice3")
