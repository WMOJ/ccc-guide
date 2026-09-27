seen = set()
seen.add(3)
seen.add(3)
seen.add(5)
print(len(seen))
print(3 in seen)
unique = {int(x) for x in input().split()}
print(sorted(unique))
