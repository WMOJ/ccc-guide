import sys


def main() -> None:
    d = sys.stdin.read().split()
    left = int(d[0])
    last = int(d[1])
    sp = [list(map(int, d[2:]))]
    LOG = len(sp[0]).bit_length()
    for k in range(1, LOG):
        a = sp[k - 1]
        b = a[1 << (k - 1):]
        r = list(map(min, a, b))
        sp.append(r)
    length = last - left + 1
    k = length.bit_length() - 1
    x = sp[k][left]
    right = last - (1 << k) + 1
    y = sp[k][right]
    print(min(x, y))


if __name__ == "__main__":
    main()
