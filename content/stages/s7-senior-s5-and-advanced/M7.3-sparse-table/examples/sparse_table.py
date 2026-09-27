import sys


def main() -> None:
    data = sys.stdin.read().split()
    idx = 0
    n = int(data[idx])
    idx += 1
    arr = list(map(int, data[idx:idx + n]))
    idx += n
    l, r = int(data[idx]), int(data[idx + 1])  # query range [l, r], inclusive

    # k columns are enough to cover ranges up to size n; n.bit_length() gives
    # the smallest k with 2^k > n, one more than actually needed, which is
    # a harmless extra column.
    k = n.bit_length()

    # table[i][j] = min of the range [i, i + 2^j)
    table = [[0] * k for _ in range(n)]

    for i in range(n):
        table[i][0] = arr[i]

    for j in range(1, k):
        half = 1 << (j - 1)
        for i in range(n - (1 << j) + 1):
            table[i][j] = min(table[i][j - 1], table[i + half][j - 1])

    # Convert the inclusive query [l, r] to a half-open length.
    length = r - l + 1
    j = length.bit_length() - 1
    result = min(table[l][j], table[r - (1 << j) + 1][j])
    print(result)


if __name__ == "__main__":
    main()
