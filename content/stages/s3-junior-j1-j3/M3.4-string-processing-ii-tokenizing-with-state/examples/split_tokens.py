import sys


def main() -> None:
    raw = sys.stdin.read()
    line = raw.rstrip("\n")
    out = []
    buf = []
    for ch in line:
        if ch == ",":
            out.append(buf)
            buf = []
        else:
            buf.append(ch)
    if buf:
        out.append(buf)
    for t in out:
        print("".join(t))


if __name__ == "__main__":
    main()
