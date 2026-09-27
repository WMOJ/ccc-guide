values = [1, 2, 4, 5]
for v in values:
    if v % 2 == 0:
        values.remove(v)
print(values)
