import sys


def expand(s, left, right):
    while left >= 0 and right < len(s) and s[left] == s[right]:
        left -= 1
        right += 1
    return left + 1, right - 1


def main() -> None:
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    s = input_data[0]

    best_left, best_right = 0, -1
    for i in range(len(s)):
        left, right = expand(s, i, i)
        if right - left > best_right - best_left:
            best_left, best_right = left, right
        if i < len(s) - 1:
            left, right = expand(s, i, i + 1)
            if right - left > best_right - best_left:
                best_left, best_right = left, right

    length = best_right - best_left + 1
    print(f"Longest palindrome in '{s}': '{s[best_left:best_right + 1]}', length {length}")


if __name__ == "__main__":
    main()
