bulbs = [1, 1, 0, 1, 1]

found_broken = False
for state in bulbs:
    if state == 0:
        found_broken = True

print(found_broken)
