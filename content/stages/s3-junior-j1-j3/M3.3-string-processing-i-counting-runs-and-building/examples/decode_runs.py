import sys


def main() -> None:
    raw = sys.stdin.read()
    s = raw.rstrip("\n")
    out = []
    i = 0
    while i < len(s):
        count = int(s[i])
        c = s[i + 1]
        out.append(c * count)
        i += 2
    print("".join(out))


if __name__ == "__main__":
    main()
