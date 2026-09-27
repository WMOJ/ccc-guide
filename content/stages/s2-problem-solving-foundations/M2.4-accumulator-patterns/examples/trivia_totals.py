scores = [7, 9, 9, 4]

total = 0
high_count = 0
for score in scores:
    total += score
    if score >= 9:
        high_count += 1

print(total)
print(high_count)
