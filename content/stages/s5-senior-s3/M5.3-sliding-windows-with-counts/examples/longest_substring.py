import sys


def main() -> None:
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    s = input_data[0]
    k = int(input_data[1])

    if not s:
        print(0)
        return

    counts = [0] * 26
    distinct = 0
    left = 0
    max_len = 0

    for right in range(len(s)):
        char_idx = ord(s[right]) - ord('a')
        if counts[char_idx] == 0:
            distinct += 1
        counts[char_idx] += 1

        while distinct > k:
            left_char_idx = ord(s[left]) - ord('a')
            counts[left_char_idx] -= 1
            if counts[left_char_idx] == 0:
                distinct -= 1
            left += 1

        max_len = max(max_len, right - left + 1)

    print(max_len)


if __name__ == "__main__":
    main()
