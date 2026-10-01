import sys


def main() -> None:
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    target = int(tokens[0])
    numbers = [int(x) for x in tokens[1:]]

    left = 0
    right = len(numbers) - 1
    result = "none"
    while left < right:
        total = numbers[left] + numbers[right]
        if total == target:
            result = f"{numbers[left]} {numbers[right]}"
            break
        elif total < target:
            left += 1
        else:
            right -= 1

    print(result)


if __name__ == "__main__":
    main()
