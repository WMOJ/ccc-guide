def matches(s):
    stack = []
    pairs = {'(': ')', '[': ']', '{': '}'}
    for c in s:
        if c in pairs:
            stack.append(c)
        else:
            if not stack or pairs[stack.pop()] != c:
                return False
    return len(stack) == 0


print(matches("(())"))
print(matches("()()"))
print(matches("([)]"))
print(matches("(()"))
