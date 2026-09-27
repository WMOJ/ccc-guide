votes = input().split()
c = {}
for v in votes:
    c[v] = c.get(v, 0) + 1
print(c)
