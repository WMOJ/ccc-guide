import sys


def main() -> None:
    raw = sys.stdin.read()
    tok = raw.split()
    n = len(tok) // 2
    jobs = []
    pos = 0
    for i in range(n):
        t = int(tok[pos])
        d = int(tok[pos + 1])
        pos += 2
        jobs.append((d, t))

    jobs.sort()

    clock = 0
    peak = -10 ** 9
    for d, t in jobs:
        clock += t
        late = clock - d
        peak = max(peak, late)

    print(peak)


if __name__ == "__main__":
    main()
