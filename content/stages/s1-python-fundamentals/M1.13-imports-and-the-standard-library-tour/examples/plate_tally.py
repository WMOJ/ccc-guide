from collections import Counter

plate_colors = ["red", "blue", "red", "green", "red", "blue"]
tally = Counter(plate_colors)

print(tally["red"])
print(tally.most_common(1))
