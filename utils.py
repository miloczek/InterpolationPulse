import numpy
from matplotlib import pyplot as plt
from typing import List, Union, Tuple, Any


def clear_list(l: List[str]) -> List[str]:
    result = []
    for item in l:
        if item != "" and item != ")":
            result.append(item)
    return result


def create_list_of_floats(l: List[str]) -> List[float]:
    result = []
    current = ""
    for index, item in enumerate(l):
        if item.isnumeric():
            current += item
        if item == "+" or item == "-":
            if current != "":
                result.append(float(current))
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


def prepare_to_show_natural_polynomial(
    x: Union[Tuple[Any, Union[Any, float]], Any], coefficients: List[float]
) -> float:
    n = len(coefficients)
    y = 0
    for i in range(n):
        y += coefficients[i] * x ** i
    return y


def prepare_to_show_newton_polynomial(
    x: Union[Tuple[Any, Union[Any, float]], Any],
    coefficients_b: List[float],
    coefficients_x: List[float],
) -> float:
    n = len(coefficients_x)
    p = 1
    y = coefficients_b[0]
    for i in range(n):
        p *= x + coefficients_x[i]
        y += coefficients_b[i + 1] * p
    return y


def show_natural_polynomial(a: float, b: float, coefficients: List[float]) -> None:
    x = numpy.linspace(a, b, 100)
    plt.plot(x, prepare_to_show_natural_polynomial(x, coefficients))
    plt.grid(True)
    plt.show()


def show_newton_polynomial(
    a: float, b: float, coefficients_b: List[float], coefficients_x: List[float]
) -> None:
    x = numpy.linspace(a, b, 100)
    plt.plot(x, prepare_to_show_newton_polynomial(x, coefficients_b, coefficients_x))
    plt.grid(True)
    plt.show()


def eval_fun(f: str, x: float) -> float:
    return eval(f)


def compute_y(x: List[float], f: str) -> Tuple[List[float]]:
    proper_f = ""
    for index, char in enumerate(f):
        if char == "^":
            proper_f += "**"
        elif char == ",":
            proper_f += "."
        elif (
            (
                index != len(f) - 1
                and (char.isnumeric() or char == "x")
                and (f[index + 1] == "x" or f[index + 1] == "(")
            )
            or (index != len(f) - 1 and char == "x" and f[index + 1].isnumeric())
            or (
                index != len(f) - 1
                and char == ")"
                and (
                    f[index + 1] == "x"
                    or f[index + 1] == "("
                    or f[index + 1].isnumeric()
                )
            )
        ):
            proper_f += char + "*"
        else:
            proper_f += char
    return [eval_fun(proper_f, xi) for xi in x], proper_f


def basic_fun_plot(x, y):
    plt.plot(x, y)
    plt.grid(True)
    plt.show()
