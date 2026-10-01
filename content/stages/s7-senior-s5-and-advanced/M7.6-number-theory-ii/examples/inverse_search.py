import sys


def main() -> None:
    raw = sys.stdin.read()
    tokens = raw.split()
    a = int(tokens[0])
    m = int(tokens[1])
    found = 0
    for x in range(1, m):
        if a * x % m == 1:
            found = x
            break
    if found == 0:
        print(f"no inverse of {a} mod {m}")
    else:
        print(f"inverse of {a} mod {m} is {found}")


if __name__ == "__main__":
    main()
