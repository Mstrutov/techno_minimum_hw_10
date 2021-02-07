def bin_search(sorted_asc_array, element):
    """
    :param sorted_asc_array: iterable object, sorted by ascending order
    :param element: element to search
    :return: position of the first element a[i] such that a[i] > element
    """
    start = -1
    end = len(sorted_asc_array)
    while start < end - 1:
        new_pos = (start + end) // 2
        if sorted_asc_array[new_pos] <= element:
            start = new_pos
        elif sorted_asc_array[new_pos] > element:
            end = new_pos
    return end
