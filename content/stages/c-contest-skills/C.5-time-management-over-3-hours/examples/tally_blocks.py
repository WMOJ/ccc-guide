def main() -> None:
    a = int(input())
    b = int(input())
    n = int(input())
    need = [a, b]
    used = [0, 0]
    done = [0, 0]
    for _ in range(n):
        p = int(input()) - 1
        m = int(input())
        used[p] += m
        if used[p] >= need[p]:
            done[p] = 1
    print(used, done)


if __name__ == "__main__":
    main()
