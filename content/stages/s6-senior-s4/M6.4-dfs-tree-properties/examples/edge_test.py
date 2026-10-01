import sys


def main() -> None:
    data = sys.stdin.read().split()
    q = int(data[0])
    pos = 1
    for _ in range(q):
        du = int(data[pos])
        dv = int(data[pos + 2])
        fv = int(data[pos + 3])
        pos += 4
        if dv == -1:
            print("tree")
        elif fv == -1:
            print("back")
        elif du < dv:
            print("forward")
        else:
            print("cross")


if __name__ == "__main__":
    main()
