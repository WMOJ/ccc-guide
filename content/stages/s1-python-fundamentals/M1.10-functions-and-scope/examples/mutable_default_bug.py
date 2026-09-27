def add_item(item, basket=[]):  # noqa: B006 (the mutable default is the bug this example shows)
    basket.append(item)
    return basket

print(add_item("apple"))
print(add_item("pear"))
