import sys


def main() -> None:
    raw = sys.stdin.read()
    s = raw.rstrip("\n")
    n = len(s)
    out = []
    i = 0
    while i < n:
        c = s[i]
        k = 1
        while i + k < n:
            if s[i+k] != c:
                break
            k += 1
        out.append(str(k))
        out.append(c)
        i += k
    print("".join(out))


if __name__ == "__main__":
    main()
