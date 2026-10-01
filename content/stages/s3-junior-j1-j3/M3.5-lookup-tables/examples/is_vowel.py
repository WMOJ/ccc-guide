import sys


def main() -> None:
    raw = sys.stdin.read()
    data = raw.split()
    if not data:
        return

    vow = {}
    for c in "aeiouAEIOU":
        vow[c] = True

    q = data[0]
    hit = vow.get(q, False)
    print(hit)


if __name__ == "__main__":
    main()
