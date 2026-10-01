import sys


def main() -> None:
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    target = int(tokens[0])
    numbers = [int(x) for x in tokens[1:]]

    position = -1
    comparisons = 0
    for i in range(len(numbers)):
        comparisons += 1
        if numbers[i] == target:
            position = i
            break

    print(position, comparisons)


if __name__ == "__main__":
    main()
