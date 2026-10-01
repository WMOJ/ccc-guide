import sys


def main() -> None:
    raw = sys.stdin.read()
    data = raw.split()
    if not data:
        return
    n = int(data[0])
    pos = 1

    high = 0
    low = 0
    all_high = True
    for i in range(n):
        score = int(data[pos])
        pos += 1
        if score > 75:
            high += 1
        else:
            low += 1
            all_high = False

    print(high, low)
    print("Yes" if all_high else "No")


if __name__ == "__main__":
    main()
