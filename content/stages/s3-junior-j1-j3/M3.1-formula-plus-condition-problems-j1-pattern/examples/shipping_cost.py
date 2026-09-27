kg = int(input())
km = int(input())

cost = kg * 2 + km // 10

if cost <= 20:
    print("Standard")
elif cost <= 50:
    print("Priority")
else:
    print("Express")
