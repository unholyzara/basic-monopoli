from dataclasses import dataclass
from typing import Callable, TYPE_CHECKING
from enum import Enum

from .utils.displays import display_money, display_properties
from .utils.inputs import select_property, get_int_input

if TYPE_CHECKING:
    from .ports.users import UserPort


@dataclass
class Action:
    label: str
    excecution: Callable[["UserPort"], bool]


def show_finance_execution(user: "UserPort"):
    print(f"User : {user.name}")
    print(f"Money: {display_money(money=user.money)}")
    user_properties = user.get_properties()
    print(f"Number of Properties: {len(user_properties)}")
    return False


def show_properties_execution(user: "UserPort"):
    print(f"Properties of User : {user.name}")
    user_properties = user.get_properties()
    display_properties(properties=user_properties)
    return False


def show_propertu_details_execution(user: "UserPort"):
    selected_property = select_property(properties=user.get_properties())
    print(f"Property selected : {selected_property.name}")
    print(str(select_property))
    return False


def go_on_execution(user: "UserPort"):
    print("Throwing dice...")
    return True


class Actions(Enum):
    FINANCE = Action(
        label="Show my finances",
        excecution=show_finance_execution,
    )
    PROPERTIES = Action(
        label="Show my properties",
        excecution=show_properties_execution,
    )
    PROPERTY_DETAIL = Action(
        label="Show property details",
        excecution=show_properties_execution,
    )
    GO_ON = Action(
        label="Resume Round",
        excecution=go_on_execution,
    )

    @classmethod
    def choose_action(cls, user: "UserPort"):
        print("What do you want to do?")
        for index, action in enumerate(cls, start=1):
            print(f"{index}) {action.value.label}")
        result = get_int_input(label="Action number: ")
        try:
            selected_action = list(cls)[result]
        except IndexError:
            print("Enter a valid action number")
            return cls.choose_action(user=user)
        else:
            return selected_action
