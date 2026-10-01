import sys


def count_compares(s, jump):
    n = len(s)
    total = 0
    i = 0
    while i < n:
        k = 1
        while i + k < n:
            total += 1
            if s[i + k] != s[i]:
                break
            k += 1
        if jump:
            i += k
        else:
            i += 1
    return total


def main() -> None:
    raw = sys.stdin.read()
    s = raw.rstrip("\n")
    slow = count_compares(s, False)
    fast = count_compares(s, True)
    print(slow, fast)


if __name__ == "__main__":
    main()
