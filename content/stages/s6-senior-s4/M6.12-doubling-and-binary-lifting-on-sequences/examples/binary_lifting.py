import sys


def main() -> None:
    data = sys.stdin.read().split()
    n = int(data[0])
    q = int(data[1])
    nxt = []
    pos = 2
    for _ in range(n):
        nxt.append(int(data[pos]))
        pos += 1

    starts = []
    ks = []
    for _ in range(q):
        s = int(data[pos])
        k = int(data[pos + 1])
        pos += 2
        starts.append(s)
        ks.append(k)

    top = max(ks)
    LOG = max(1, top.bit_length())
    up = [nxt]
    for k in range(1, LOG):
        prev = up[k - 1]
        row = [prev[x] for x in prev]
        up.append(row)

    out = []
    for i in range(q):
        here = starts[i]
        todo = ks[i]
        for k in range(LOG):
            if (todo >> k) & 1:
                here = up[k][here]
        out.append(str(here))
    text = "\n".join(out)
    sys.stdout.write(text + "\n")


if __name__ == "__main__":
    main()
