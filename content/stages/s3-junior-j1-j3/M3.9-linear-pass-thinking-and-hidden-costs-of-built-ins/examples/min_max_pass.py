import sys


def main() -> None:
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    numbers = [int(x) for x in tokens]

    min_val = numbers[0]
    max_val = numbers[0]
    for num in numbers[1:]:
        min_val = min(min_val, num)
        max_val = max(max_val, num)

    print(min_val, max_val)


if __name__ == "__main__":
    main()
