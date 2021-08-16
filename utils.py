import tkinter as tk
from tkinter.constants import TRUE
from typing import Any, List, Tuple, Union


import numpy
from matplotlib import pyplot as plt


SMALL_FLOAT = numpy.finfo(float).eps


def clear_win(window: tk.Tk) -> None:
    """Pozbywa się wszyskich elementów w oknie."""
    for widgets in window.winfo_children():
        widgets.destroy()


def clear_list(l: List[str]) -> List[str]:
    """Wyrzuca z listy puste znaki i nawiasy."""
    result = []
    for item in l:
        if item != "" and item != ")":
            result.append(item)
    return result


def create_list_of_floats(l: List[str]) -> List[float]:
    """Przerabia listę stringów na listę floatów."""
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
    """Parsuje wielomian, wstawiając jedynki w odpowiednich miejscach."""
    new_s = ""
    if s[0] == "(":
        new_s += "1"
    for index, char in enumerate(s):
        if char == "(" and (s[index - 1] != ")") and (not s[index - 1].isnumeric()):
            new_s += "1"
        new_s += char
    return new_s


def return_next_not_empty_char(word: str) -> str:
    return next(s for s in word.split() if s)


def prepare_to_show_natural_polynomial(
    x: Union[Tuple[Any, Union[Any, float]], Any], coefficients: List[float]
) -> float:
    """Na podstawie współczynników, zwraca wielomian w postaci naturalnej."""
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
    """Na podstawie współczynników, zwraca wielomian w postaci Newtona."""
    n = len(coefficients_x)
    p = 1
    y = coefficients_b[0]
    for i in range(n):
        p *= x + coefficients_x[i]
        y += coefficients_b[i + 1] * p
    return y


def show_natural_polynomial(a: float, b: float, coefficients: List[float]) -> None:
    """Generuje wielomian w postaci naturalnej."""
    x = numpy.linspace(a, b, 100)
    plt.plot(x, prepare_to_show_natural_polynomial(x, coefficients))
    plt.grid(True)
    plt.show()


def show_newton_polynomial(
    a: float, b: float, coefficients_b: List[float], coefficients_x: List[float]
) -> None:
    """Generuje wielomian w postaci Newtona."""
    x = numpy.linspace(a, b, 100)
    plt.plot(x, prepare_to_show_newton_polynomial(x, coefficients_b, coefficients_x))
    plt.grid(True)
    plt.show()


def eval_fun(f: str, x: Union[float, numpy.ndarray]) -> float:
    """Oblicza funkcję f na podstawie zaaplikowanego x."""
    return eval(f)


def eval_derivative_fun(f: str, x: float, delta: float = 0.001) -> float:
    """Oblicza wartość pochodnej funkcji dla wybranej delty."""
    return (eval_fun(f, x + delta) - eval_fun(f, x)) / delta


def eval_fun_with_prec(f: str, x: float, precision: int) -> float:
    """Oblicza funkcję f na podstawie zaaplikowanego x z wybraną precyzją."""
    return round(eval(f), precision)


def eval_derivative_fun_with_prec(
    f: str, x: float, precision: int, delta: float = 0.001
) -> float:
    """Oblicza wartość pochodnej funkcji dla wybranej delty z precyzją."""
    return round(
        (
            eval_fun_with_prec(f, x + delta, precision)
            - eval_fun_with_prec(f, x, precision)
        )
        / delta,
        precision,
    )


def compute_y(x: List[float], f: str) -> Tuple[List[float]]:
    """Parsuje i oblicza ostateczną wartość funkcji."""
    proper_f = ""
    negative_power = False
    for index, char in enumerate(f):
        if char == "^":
            if return_next_not_empty_char(f[index + 1 :]).startswith(
                "-"
            ) or return_next_not_empty_char(f[index + 1 :]).startswith("("):
                negative_power = True
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

    if not negative_power:
        return [eval_fun(proper_f, xi) for xi in x], proper_f
    else:
        return [
            eval_fun(proper_f, xi)
            if xi != float(0)
            else eval_fun(proper_f, SMALL_FLOAT)
            for xi in x
        ], proper_f


def compute_y_with_prec(x: List[float], f: str, precision: int) -> Tuple[List[float]]:
    """Parsuje i oblicza ostateczną wartość funkcji z wybraną precyzją."""
    proper_f = ""
    negative_power = False
    for index, char in enumerate(f):
        if char == "^":
            if return_next_not_empty_char(f[index + 1 :]).startswith(
                "-"
            ) or return_next_not_empty_char(f[index + 1 :]).startswith("("):
                negative_power = True
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
    if not negative_power:
        return [
            eval_fun_with_prec(proper_f, round(xi, precision), precision) for xi in x
        ], proper_f
    else:
        return [
            eval_fun_with_prec(proper_f, round(xi, precision), precision)
            if xi != float(0)
            else eval_fun_with_prec(proper_f, round(SMALL_FLOAT, precision), precision)
            for xi in x
        ], proper_f


def basic_fun_plot(x: Union[Tuple[Any, Union[Any, float]], Any], y: float) -> None:
    """Generuje wykres funkcji na podstawie x i y."""
    plt.plot(x, y)
    plt.grid(True)
    plt.show()


def compare_fun_and_interpolation_plot(
    x: Union[Tuple[Any, Union[Any, float]], Any], y1: float, y2: float
) -> None:
    """Generuje wykres porównawczy funkcji wejściowej i wielomianu interpolacyjnego"""
    fig, axs = plt.subplots(2)
    for ax in fig.axes:
        ax.grid(True)
    fig.suptitle("Wykres porównawczy")
    axs[0].plot(x, y1)
    axs[1].plot(x, y2)
    plt.show()
