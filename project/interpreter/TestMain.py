from Interpreter import InterpretFunction


dir = "demo\decompiled\classes"
file = "com\example\Main"

res = InterpretFunction(
    dir=dir,
    file=file,
    printDebug=True,
)

print(res)
