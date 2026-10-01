import sys


def main() -> None:
    raw = sys.stdin.read()
    data = raw.split()
    n = int(data[0])
    i = int(data[1])
    j = int(data[2])

    up = []
    while i <= n:
        up.append(i)
        low = i & -i
        i += low

    down = []
    while j > 0:
        down.append(j)
        low = j & -j
        j -= low

    print("update visits", up)
    print("query visits", down)


if __name__ == "__main__":
    main()
