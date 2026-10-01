import sys


def main() -> None:
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    numbers = [int(x) for x in tokens]

    seen = set()
    first_dup = -1
    for num in numbers:
        if num in seen:
            first_dup = num
            break
        seen.add(num)

    print(first_dup)


if __name__ == "__main__":
    main()
