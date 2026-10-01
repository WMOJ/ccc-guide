import sys


def main() -> None:
    raw = sys.stdin.read()
    line = raw.rstrip("\n")
    tokens = []
    buf = []
    i = 0
    while i < len(line):
        if line[i:i + 2] == "::":
            tokens.append("".join(buf))
            buf = []
            i += 2
        else:
            buf.append(line[i])
            i += 1
    tokens.append("".join(buf))
    for token in tokens:
        print(token)


if __name__ == "__main__":
    main()
