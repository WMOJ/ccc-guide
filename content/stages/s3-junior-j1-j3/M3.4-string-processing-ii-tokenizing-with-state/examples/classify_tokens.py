import sys


def main() -> None:
    raw = sys.stdin.read()
    line = raw.rstrip("\n")
    tokens = []
    buf = []
    mode = ""
    for char in line:
        is_sign = char in "+-"
        if char.isalpha():
            kind = "letters"
        else:
            kind = "number"
        starts_new = is_sign or kind != mode
        if starts_new and buf:
            tokens.append("".join(buf))
            buf = []
        mode = kind
        buf.append(char)
    if buf:
        tokens.append("".join(buf))
    for token in tokens:
        print(token)


if __name__ == "__main__":
    main()
