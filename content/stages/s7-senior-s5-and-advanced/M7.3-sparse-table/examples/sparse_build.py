import sys


def main() -> None:
    data = sys.stdin.read().split()
    n = int(data[0])
    a = []
    pos = 1
    for _ in range(n):
        a.append(int(data[pos]))
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
            row.append(min(x, y))
        sp.append(row)

    out = []
    for k in range(LOG):
        out.append(f"sp[{k}] = {sp[k]}")
    sys.stdout.write("\n".join(out) + "\n")


if __name__ == "__main__":
    main()
