nums = [int(x) for x in input().split()]
print(sum(nums))
print(sum(x for x in nums if x > 0))
print(any(x < 0 for x in nums))
print(all(x > 0 for x in nums))
