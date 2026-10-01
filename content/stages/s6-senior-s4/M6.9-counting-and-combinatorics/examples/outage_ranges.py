import sys


def main() -> None:
    data = sys.stdin.read().split()
    n = int(data[0])
    readings = list(map(int, data[1:1 + n]))

    total = n * (n + 1) // 2
    clean = 0
    run = 0
    for value in readings:
        if value == 0:
            run = 0
        else:
            run += 1
        clean += run

    print(total - clean)


if __name__ == "__main__":
    main()
