import sys


def main() -> None:
    data = sys.stdin.read().split()
    n = int(data[0])
    k = int(data[1])
    pos = 2
    bit = [0] * n
    for i in range(k):
        room = int(data[pos])
        bit[room] = 1 << i
        pos += 1

    mask = 0
    for x in data[pos:]:
        room = int(x)
        mask = mask | bit[room]
        print(room, mask)


if __name__ == "__main__":
    main()
