from typing import TypeVar, TYPE_CHECKING

from .displays import display_properties

if TYPE_CHECKING:
    from basic_monopoli.domain.ports.boxes import BoxPortType

    T = TypeVar("T", bound=BoxPortType)

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
        users_number = int(input(label))
    except ValueError:
        print("Enter a correct number")
        return get_int_input(label=label)
    else:
        return users_number


def select_properties(
    properties: list["T"],
    message: str = "Select properties (1,2,3,...): ",
) -> list["T"]:
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
            return select_properties(properties=properties, message=message)
        else:
            return selected_properties


def select_property(
    properties: list["T"], message: str = "Select property: "
) -> "T":
    display_properties(properties=properties)
    index = get_int_input(label=message)
    try:
        selected_property = properties[index]
    except IndexError:
        print("Add a correct number")
        return select_property(properties=properties, message=message)
    else:
        return selected_property
