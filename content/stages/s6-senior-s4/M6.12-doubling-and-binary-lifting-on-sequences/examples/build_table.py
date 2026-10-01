import sys


def main() -> None:
    data = sys.stdin.read().split()
    n = int(data[0])
    nxt = []
    pos = 2
    for _ in range(n):
        nxt.append(int(data[pos]))
        pos += 1
    top = int(data[pos + 1])

    LOG = max(1, top.bit_length())
    up = [nxt]
    for k in range(1, LOG):
        prev = up[k - 1]
        row = [prev[x] for x in prev]
        up.append(row)

    out = []
    for k in range(LOG):
        out.append(f"up[{k}] = {up[k]}")
    sys.stdout.write("\n".join(out) + "\n")


if __name__ == "__main__":
    main()
