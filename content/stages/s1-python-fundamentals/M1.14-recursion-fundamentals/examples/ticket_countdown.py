def countdown(n):
    if n == 0:
        return []
    rest = countdown(n - 1)
    return [n] + rest


print(countdown(3))
