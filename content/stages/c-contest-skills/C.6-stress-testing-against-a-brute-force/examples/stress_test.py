import random


def brute_force_max_sum(arr):
    """Find the maximum sum of any contiguous subarray (brute force)."""
    max_sum = arr[0]
    for i in range(len(arr)):
        current_sum = 0
        for j in range(i, len(arr)):
            current_sum += arr[j]
            max_sum = max(max_sum, current_sum)
    return max_sum


def fast_max_sum(arr):
    """Find the maximum sum of any contiguous subarray (Kadane's algorithm)."""
    max_sum = arr[0]
    current_sum = arr[0]
    for i in range(1, len(arr)):
        current_sum = max(arr[i], current_sum + arr[i])
        max_sum = max(max_sum, current_sum)
    return max_sum


# Set seed for reproducible random inputs
random.seed(42)

mismatches = 0
for test_num in range(1000):
    n = random.randint(2, 20)
    arr = [random.randint(-100, 100) for _ in range(n)]

    brute = brute_force_max_sum(arr)
    fast = fast_max_sum(arr)

    if brute != fast:
        mismatches += 1
        print(f"Test {test_num}: MISMATCH")
        print(f"  Input: {arr}")
        print(f"  Brute force: {brute}")
        print(f"  Fast solution: {fast}")
        print()

if mismatches == 0:
    print("All 1000 tests passed!")
else:
    print(f"{mismatches} test(s) failed out of 1000.")
