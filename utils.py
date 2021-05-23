def clear_list(l):
    result = []
    for item in l:
        if item != "" and item != ")":
            result.append(item)
    return result

def create_list_of_ints(l):
    result = []
    current = ""
    for index, item in enumerate(l):
        if item.isnumeric():
            current += item
        if item == "+" or item == "-":
            result.append(int(current))
            current = item
        if index == len(l) - 1:
            result.append(current)
    return result
