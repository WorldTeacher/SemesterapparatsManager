from typing import List, Tuple

from natsort import natsorted


def custom_sort(unsorted: List[Tuple[str, int, int]]) -> List[Tuple[str, int, int]]:
    """Sort a list of semesters in the format "SoSe n" and "WiSe n/n+1" in the correct order.
    Where n == year in 2 digit format

    Args:
    ----
        unsorted (list[tuple]): List of semesters in the format "SoSe n" and "WiSe n/n+1"

    Returns:
    -------
        ret (list[tuple]): Sorted list in correct order of WiSe n/n+1 and SoSe n
    """
    summer = natsorted([i for i in unsorted if "SoSe" in i[0]])
    winter = natsorted([i for i in unsorted if "WiSe" in i[0]])
    summer = natsorted(summer, key=lambda x: x[0])
    winter = natsorted(winter, key=lambda x: x[0])

    # Merge the lists
    ret = []
    i = 0
    j = 0
    while i < len(summer) and j < len(winter):
        if summer[i][0][5:] <= winter[j][0][5:]:
            ret.append(summer[i])
            i += 1
        else:
            ret.append(winter[j])
            j += 1

    # Append the remaining items
    while i < len(summer):
        ret.append(summer[i])
        i += 1
    while j < len(winter):
        ret.append(winter[j])
        j += 1

    return ret

    # Test the function

    pass


if __name__ == "__main__":
    unsorted = [
        ("WiSe 23/24", 7, 5),
        ("SoSe 23", 5, 0),
        ("SoSe 22", 1, 0),
        ("WiSe 22/23", 1, 0),
        ("SoSe 15", 1, 0),
    ]

    print(custom_sort(unsorted))
