from Util import StackFrame
from Interpreter import InterpretFunction


def InvokeStatic(dir, operandStack, printDebug, heap, method):
    sf = StackFrame()
    for i in reversed(range(len(method["args"]))):
        sf.set(i, operandStack.pop())

    res = InterpretFunction(
        dir=dir,
        file=method["ref"]["name"],
        function=method["name"],
        stackFrame=sf,
        heap=heap,
        printDebug=printDebug,
    )

    return res
