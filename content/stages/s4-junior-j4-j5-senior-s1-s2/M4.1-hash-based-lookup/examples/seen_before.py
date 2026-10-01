import sys


def main() -> None:
    raw = sys.stdin.read()
    data = raw.split()
    if not data:
        return

    n = int(data[0])
    vals = data[1:n + 1]

    seen = set()
    res = []
    for v in vals:
        if v in seen:
            label = "seen"
        else:
            label = "new"
            seen.add(v)
        res.append(label)

    for r in res:
        print(r)


if __name__ == "__main__":
    main()
