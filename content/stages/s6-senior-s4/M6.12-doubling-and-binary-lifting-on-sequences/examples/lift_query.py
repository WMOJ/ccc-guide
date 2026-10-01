import sys


def main() -> None:
    d = sys.stdin.read().split()
    todo = int(d[0])
    here = int(d[1])
    up = [list(map(int, d[2:]))]
    LOG = todo.bit_length()
    for k in range(1, LOG):
        p = up[k - 1]
        row = [p[x] for x in p]
        up.append(row)
    for k in range(LOG):
        if (todo >> k) & 1:
            here = up[k][here]
    print(here)


if __name__ == "__main__":
    main()
