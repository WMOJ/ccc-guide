def count_up(n, target):
    if n == target:
        return
    count_up(n + 1, target)


count_up(0, 2000)
