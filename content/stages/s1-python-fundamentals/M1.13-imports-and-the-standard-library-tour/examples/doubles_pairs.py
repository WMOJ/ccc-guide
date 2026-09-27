from itertools import combinations

players = ["Amir", "Bo", "Chen"]

for pair in combinations(players, 2):
    print(pair)
