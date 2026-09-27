import random

n = 1000
target = 10000
prices = [random.randint(1, 10000) for _ in range(n)]

print(n, target)
line = ""
first = True
for p in prices:
    if not first:
        line += " "
    line += str(p)
    first = False
print(line)
