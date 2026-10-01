import sys


def main() -> None:
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    pos = 0
    text = input_data[pos]
    pos += 1
    i = int(input_data[pos])
    pos += 1
    j = int(input_data[pos])
    pos += 1
    length = int(input_data[pos])
    pos += 1

    base = 31
    mod = (1 << 61) - 1
    n = len(text)

    powers = [1] * (n + 1)
    for k in range(1, n + 1):
        powers[k] = (powers[k - 1] * base) % mod

    prefix_hash = [0] * (n + 1)
    for k in range(n):
        prefix_hash[k + 1] = (prefix_hash[k] * base + ord(text[k])) % mod

    def window_hash(start: int, length: int) -> int:
        end = start + length
        return (prefix_hash[end] - prefix_hash[start] * powers[length]) % mod

    hash_a = window_hash(i, length)
    hash_b = window_hash(j, length)

    if hash_a != hash_b:
        print("different")
        return

    if text[i : i + length] == text[j : j + length]:
        print("equal")
    else:
        print("collision")


if __name__ == "__main__":
    main()
