from z3 import *

a = Int("a")
b = Int("b")
x1 = Int("x1")
y1 = Int("y1")
e1 = x1 == a * 20
e2 = y1 == b + 5
e3 = y1 < x1
solver = Solver()
solver.add(e1, e2, e3)
result = solver.check()
print(result)
if result == sat:
    print(solver.model())
