nums = [int(x) for x in input().split()]
print(sorted(nums))
print(list(reversed(nums)))
for i, x in enumerate(nums):
    print(i, x)
