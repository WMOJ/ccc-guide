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


n = 9875
print(digital_root_bruteforce(n))
