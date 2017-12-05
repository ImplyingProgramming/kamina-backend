from inspect import getmembers
from pprint import pprint


def var_dump(var) -> None:
    pprint(getmembers(var))
