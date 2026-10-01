import sys


def main() -> None:
    data = sys.stdin.read().split()
    n = int(data[0])
    values = [0]
    for k in range(n):
        values.append(int(data[1 + k]))

    width = n.bit_length()
    for i in range(1, n + 1):
        low = i & -i
        start = i - low + 1
        total = sum(values[start:i + 1])
        bits = bin(i)[2:].zfill(width)
        print(i, bits, low, str(start) + ".." + str(i), total)


if __name__ == "__main__":
    main()
