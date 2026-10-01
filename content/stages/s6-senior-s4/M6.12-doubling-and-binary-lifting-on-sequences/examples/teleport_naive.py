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

    out = []
    hops = 0
    for _ in range(q):
        here = int(data[pos])
        k = int(data[pos + 1])
        pos += 2
        for _ in range(k):
            here = nxt[here]
            hops += 1
        out.append(str(here))
    out.append(f"hops made: {hops}")
    sys.stdout.write("\n".join(out) + "\n")


if __name__ == "__main__":
    main()
