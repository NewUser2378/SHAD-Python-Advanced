def filter_list_by_list(
    lst_a: list[int] | range, lst_b: list[int] | range
) -> list[int]:
    """
    Filter first sorted list by other sorted list
    :param lst_a: first sorted list
    :param lst_b: second sorted list
    :return: filtered sorted list
    """
    ans = []
    if len(lst_b) == 0:
        for j in range(len(lst_a)):
            ans.append(lst_a[j])
        return ans
    k = 0
    for i in range(len(lst_a)):
        while k < len(lst_b) - 1 and lst_b[k] < lst_a[i]:
            k += 1
            print(k)
        if lst_a[i] != lst_b[k]:
            ans.append(lst_a[i])
    return ans
