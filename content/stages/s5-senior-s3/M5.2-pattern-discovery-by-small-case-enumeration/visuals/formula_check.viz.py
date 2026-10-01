import vizrec as vz


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


rec = vz.Recorder()
data = rec.stdin.split()
limit = int(data[0])

brute = [digital_root_bruteforce(n) for n in range(1, limit + 1)]
formula = [digital_root_formula(n) for n in range(1, limit + 1)]
match = all(b == f for b, f in zip(brute, formula))

rec.step(
    f"Brute force and 1 + (N - 1) % 9 agree for every N from 1 to {limit}.",
    brute=vz.array(brute, states=["done"] * limit),
    formula=vz.array(formula, states=["done"] * limit),
)
rec.output("all match\n" if match else "not all match\n")
rec.done()
