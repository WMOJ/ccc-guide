import sys

# Python version of the sum program
def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    total = 0
    for i in range(1, n + 1):
        total += int(data[i])
    sys.stdout.write(f"{total}\n")

if __name__ == "__main__":
    main()
