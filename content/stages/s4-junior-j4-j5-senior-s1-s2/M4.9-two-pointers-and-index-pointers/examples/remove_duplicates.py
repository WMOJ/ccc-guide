def remove_duplicates(arr):
    if not arr:
        return 0
    write = 0
    for read in range(1, len(arr)):
        if arr[read] != arr[write]:
            write += 1
            arr[write] = arr[read]
    return write + 1


arr = [1, 1, 2, 2, 3]
length = remove_duplicates(arr)
print(arr[:length])
