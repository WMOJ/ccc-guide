weight = int(input())
distance = int(input())

cost = weight * 2 + distance // 10

if cost <= 20:
    print("Standard")
elif cost <= 50:
    print("Priority")
else:
    print("Express")
