import numpy
from matplotlib import pyplot as plt
from typing import List, Union, Tuple, Any


def clear_list(l: List[str]) -> List[str]:
    result = []
    for item in l:
        if item != "" and item != ")":
            result.append(item)
    return result


def create_list_of_ints(l: List[str]) -> List[int]:
    result = []
    current = ""
    for index, item in enumerate(l):
        if item.isnumeric():
            current += item
        if item == "+" or item == "-":
            if current != "":
                result.append(int(current))
            current = item
        if index == len(l) - 1:
            result.append(current)
    return result


def make_ones(s: str) -> str:
    new_s = ""
    if s[0] == "(":
        new_s += "1"
    for index, char in enumerate(s):
        if char == "(" and (s[index - 1] != ")") and (not s[index - 1].isnumeric()):
            new_s += "1"
        new_s += char
    return new_s


def prepare_to_show_natural_polynomial(x: Union[Tuple[Any, Union[Any, float]], Any], coefficients: List[int]) -> int:
    n = len(coefficients)
    y = 0
    for i in range(n):
        y += coefficients[i] * x ** i
    return y


def prepare_to_show_newton_polynomial(x: Union[Tuple[Any, Union[Any, float]], Any], coefficients_b: List[int], coefficients_x: List[int]) -> int:
    n = len(coefficients_x)
    p = 1
    y = coefficients_b[0]
    for i in range(n):
        p *= (x + coefficients_x[i])
        y += coefficients_b[i+1] * p
    return y


def show_natural_polynomial(a: int, b: int, coefficients: List[int]) -> None:
    x = numpy.linspace(a, b, 100)
    plt.plot(x, prepare_to_show_natural_polynomial(x, coefficients))
    plt.grid(True)
    plt.show()


def show_newton_polynomial(a: int, b: int, coefficients_b: List[int], coefficients_x: List[int]) -> None:
    x = numpy.linspace(a, b, 100)
    plt.plot(x, prepare_to_show_newton_polynomial(
        x, coefficients_b, coefficients_x))
    plt.grid(True)
    plt.show()


def eval_fun(f: str, x: int) -> int:
    return eval(f)


def compute_y(x: List[int], f: str) -> List[int]:
    proper_f = ""
    for index, char in enumerate(f):
        pass
    print(eval_fun(f, x[0]))
