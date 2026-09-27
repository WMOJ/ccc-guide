import sys


def main() -> None:
    input_data = sys.stdin.read().split()
    n = int(input_data[0])
    a = [int(input_data[i + 1]) for i in range(n)]
    target = int(input_data[n + 1])

    # Mean-shift: a subarray's average equals target exactly when the sum of
    # (element - target) over that subarray is 0. Counting zero-sum
    # subarrays only needs a hash map keyed by prefix sum, since two equal
    # prefix sums mean the subarray between them sums to zero.
    shifted = [x - target for x in a]

    count_by_prefix = {0: 1}  # the empty prefix, before any elements
    prefix = 0
    answer = 0

    for val in shifted:
        prefix += val
        answer += count_by_prefix.get(prefix, 0)
        count_by_prefix[prefix] = count_by_prefix.get(prefix, 0) + 1

    print(answer)


if __name__ == "__main__":
    main()
