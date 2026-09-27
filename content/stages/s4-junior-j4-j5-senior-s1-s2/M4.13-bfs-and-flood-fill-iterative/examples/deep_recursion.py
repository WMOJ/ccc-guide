def fill(c):
    seen[c] = True
    if c + 1 < n and not seen[c + 1]:
        fill(c + 1)


n = 3000
seen = [False] * n
fill(0)
print("done")
