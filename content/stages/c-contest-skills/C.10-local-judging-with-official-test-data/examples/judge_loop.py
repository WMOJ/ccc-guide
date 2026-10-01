import sys


def main() -> None:
    raw = sys.stdin.read()
    tokens = raw.split()
    t = int(tokens[0])
    for k in range(1, t + 1):
        a = 2 * k - 1
        data = int(tokens[a])
        want = tokens[a + 1]
        got = str(2 * data)
        if got == want:
            print(k, "matches")
        else:
            print(k, "differs")


if __name__ == "__main__":
    main()
