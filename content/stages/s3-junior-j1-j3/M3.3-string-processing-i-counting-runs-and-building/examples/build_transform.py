import sys

VOWELS = "aeiou"


def main() -> None:
    raw = sys.stdin.read()
    s = raw.rstrip("\n")
    parts = []
    for char in s:
        if char in VOWELS:
            parts.append("*")
        else:
            parts.append(char)
    print("".join(parts))


if __name__ == "__main__":
    main()
