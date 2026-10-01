import sys


def main() -> None:
    raw = sys.stdin.read()
    s = raw.rstrip("\n")
    i = 0
    while i < len(s):
        current_char = s[i]
        count = 1
        while i + count < len(s) and s[i + count] == current_char:
            count += 1
        print(current_char, count)
        i += count


if __name__ == "__main__":
    main()
