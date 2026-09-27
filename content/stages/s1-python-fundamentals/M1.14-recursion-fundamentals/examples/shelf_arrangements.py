def books_on_shelf(n):
    if n == 0:
        return 1
    return n * books_on_shelf(n - 1)


print(books_on_shelf(4))
