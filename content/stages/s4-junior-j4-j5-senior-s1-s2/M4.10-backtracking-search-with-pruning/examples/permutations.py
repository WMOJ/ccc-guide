def permutations(elements):
    result = []
    
    def backtrack(current, remaining):
        if not remaining:
            result.append(current[:])
            return
        for i in range(len(remaining)):
            current.append(remaining[i])
            backtrack(current, remaining[:i] + remaining[i+1:])
            current.pop()
    
    backtrack([], elements)
    return result


perms = permutations([1, 2, 3])
for p in perms:
    print(p)
