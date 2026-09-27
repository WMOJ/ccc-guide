names = input().split()
scores = [int(x) for x in input().split()]
for name, score in zip(names, scores):
    print(name, score)
