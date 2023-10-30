stack = ["a","b","c","d","e","f"]
byteObj={"words": 2}

vals = stack[-byteObj["words"]:]
stack = stack[: len(stack) - byteObj["words"]]
for v in vals:
    stack.append(v)
    stack.append(v)

print(stack)