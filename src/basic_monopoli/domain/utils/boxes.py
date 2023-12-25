from functools import reduce

from ..ports.boxes import PropertyBoxPort


def get_properties_value(properties: list["PropertyBoxPort"]):
    prices = map(lambda box: box.get_price(), properties)
    value = reduce(lambda tot, price: tot + price, prices, 0.0)
    return value
