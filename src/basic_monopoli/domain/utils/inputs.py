from typing import TypeVar

from .displays import display_properties
from ..ports.boxes import BoxPortType

YES = "Y"
NO = "N"


def get_yes_no_inpout(label: str) -> bool:
    result = input(label + f' ("{YES}"/"{NO}")')
    if result.upper() in [YES, NO]:
        return result.upper() == YES
    else:
        print("Enter a correct answer")
        return get_yes_no_inpout(label=label)


def get_int_input(label: str) -> int:
    try:
        users_number = int(input("How many users?"))
    except ValueError:
        print("Enter a correct number")
        return get_int_input(label=label)
    else:
        return users_number


T = TypeVar("T", bound=BoxPortType)


def select_properties(
    properties: list[T],
    message: str = "Select properties (1,2,3,...): ",
) -> list[T]:
    display_properties(properties=properties)
    result_str = input(message)
    result = result_str.split(",")
    try:
        selected_index = list(map(int, result))
    except ValueError:
        print("Add a correct list of indexes")
        return select_properties(properties=properties)
    else:
        try:
            selected_properties = list(
                map(lambda index: properties[index], selected_index)
            )
        except IndexError:
            print("Add a correct list of indexes")
            return select_properties(properties=properties)
        else:
            return selected_properties
