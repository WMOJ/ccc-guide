import sys


def digit_sum(n):
    total = 0
    while n > 0:
        total += n % 10
        n //= 10
    return total


def digital_root_bruteforce(n):
    while n >= 10:
        n = digit_sum(n)
    return n


def digital_root_formula(n):
    return 1 + (n - 1) % 9


def main() -> None:
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    limit = int(input_data[0])
    mismatches = 0
    for n in range(1, limit + 1):
        if digital_root_bruteforce(n) != digital_root_formula(n):
            mismatches += 1

    if mismatches == 0:
        print("all match")
    else:
        print(f"{mismatches} mismatches")


if __name__ == "__main__":
    main()
