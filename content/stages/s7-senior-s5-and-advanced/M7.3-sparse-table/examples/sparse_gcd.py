import sys
from math import gcd


def main() -> None:
    data = sys.stdin.read().split()
    n = int(data[0])
    a = []
    pos = 1
    for _ in range(n):
        a.append(int(data[pos]))
        pos += 1
    q = int(data[pos])
    pos += 1

    LOG = n.bit_length()
    sp = [a]
    for k in range(1, LOG):
        prev = sp[k - 1]
        half = 1 << (k - 1)
        count = n - (1 << k) + 1
        row = []
        for i in range(count):
            x = prev[i]
            y = prev[i + half]
            row.append(gcd(x, y))
        sp.append(row)

    out = []
    for _ in range(q):
        left = int(data[pos])
        last = int(data[pos + 1])
        pos += 2
        length = last - left + 1
        k = length.bit_length() - 1
        second = last - (1 << k) + 1
        front = sp[k][left]
        back = sp[k][second]
        out.append(str(gcd(front, back)))
    sys.stdout.write("\n".join(out) + "\n")


if __name__ == "__main__":
    main()
