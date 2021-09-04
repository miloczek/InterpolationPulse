import math
import tkinter as tk
from tkinter import Label, constants
from tkinter.constants import TRUE
from typing import Any, List, Tuple, Union
import random


import numpy
from numpy.core.fromnumeric import var
from numpy.polynomial import Chebyshev
from matplotlib import pyplot as plt


SMALL_FLOAT = numpy.finfo(float).eps
PI = math.pi


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
    x = numpy.linspace(a, b, 10000)
    plt.plot(x, prepare_to_show_natural_polynomial(x, coefficients))
    plt.grid(True)
    plt.show()


def show_newton_polynomial(
    a: float, b: float, coefficients_b: List[float], coefficients_x: List[float]
) -> None:
    """Generuje wielomian w postaci Newtona."""
    x = numpy.linspace(a, b, 10000)
    plt.plot(x, prepare_to_show_newton_polynomial(x, coefficients_b, coefficients_x))
    plt.grid(True)
    plt.show()


def eval_fun(f: str, x: Union[float, numpy.ndarray]) -> float:
    """Oblicza funkcję f na podstawie zaaplikowanego x."""
    return eval(f)


def eval_fun_with_prec(f: str, x: float, precision: int) -> float:
    """Oblicza funkcję f na podstawie zaaplikowanego x z wybraną precyzją."""
    return round(eval(f), precision)


def add_coma_to_str(xs: str) -> str:
    xs = xs if xs.endswith(",") else xs + ","
    return xs


def check_if_nodes_and_values_are_equal(x: str, y: str, y_prim: str) -> bool:
    x, y, y_prim = add_coma_to_str(x), add_coma_to_str(y), add_coma_to_str(y_prim)
    return [len(x.split(",")), len(y.split(",")), len(y_prim.split(","))].count(
        len(x.split(","))
    ) == 3


def str_to_float_list(xs: str) -> List[float]:
    return [float(xi) for xi in xs.split(",") if xi != " " and xi != ""]


def generate_vals_and_derives(xs: List[float], fun_type: str) -> Tuple[str, str]:
    y_str, y_prim_str = "", ""
    if fun_type == "4x^2 - 15x + 2":
        y = [4 * xi ** 2 - 15 * xi + 2 for xi in xs]
        y_prim = [8 * xi - 15 for xi in xs]
    elif fun_type == "0.78^x":
        y = [0.78 ** xi for xi in xs]
        y_prim = [xi * 0.78 ** (xi - 1) for xi in xs]
    elif fun_type == "-7x^3 + 12x^2 - 19x + 3":
        y = [-7 * xi ** 3 + 12 * xi ** 2 - 19 * xi + 3 for xi in xs]
        y_prim = [-21 * xi ** 2 + 24 * xi - 19 for xi in xs]
    elif fun_type == "1/(1+25x^2)":
        y = [1 / (1 + 25 * xi ** 2) for xi in xs]
        y_prim = [-(50 * xi) / (1 + 25 * xi ** 2) ** 2 for xi in xs]
    elif fun_type == "2x^3/3":
        y = [(8 * xi ** 3) / 12 for xi in xs]
        y_prim = [2 * xi ** 2 for xi in xs]
    for i in range(len(y)):
        y_str += f"{y[i]}, "
        y_prim_str += f"{y_prim[i]}, "
    return y_str, y_prim_str


def compute_y(x: List[float], f: str) -> Tuple[List[float]]:
    """Parsuje i oblicza ostateczną wartość funkcji."""
    proper_f = ""
    negative_power_or_div = False
    f = f.replace(" ", "")
    for index, char in enumerate(f):
        if char == "p":
            proper_f += "numpy.pi"
        elif char == "i" or char == " ":
            continue
        elif char == "^":
            if return_next_not_empty_char(f[index + 1 :]).startswith(
                "-"
            ) or return_next_not_empty_char(f[index + 1 :]).startswith("("):
                negative_power_or_div = True
            proper_f += "**"
        elif char == ",":
            proper_f += "."
        elif char == "/":
            proper_f += "/"
            negative_power_or_div = True
        elif (
            (
                index != len(f) - 1
                and (char.isnumeric() or char == "x")
                and (f[index + 1] == "x" or f[index + 1] == "(" or f[index + 1] == "p")
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
    if not negative_power_or_div:
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
    negative_power_or_div = False
    f = f.replace(" ", "")
    for index, char in enumerate(f):
        if char == "p":
            proper_f += "numpy.pi"
        elif char == "i" or char == " ":
            continue
        elif char == "^":
            if return_next_not_empty_char(f[index + 1 :]).startswith(
                "-"
            ) or return_next_not_empty_char(f[index + 1 :]).startswith("("):
                negative_power_or_div = True
            proper_f += "**"
        elif char == ",":
            proper_f += "."
        elif char == "/":
            proper_f += "/"
            negative_power_or_div = True
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
    if not negative_power_or_div:
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
    x: Union[Tuple[Any, Union[Any, float]], Any],
    y1: List[float],
    y2: List[float],
    delta_y: List[float],
    var_nodes: bool,
    nodes_x,
    nodes_y,
) -> None:
    """Generuje wykres porównawczy funkcji wejściowej i wielomianu interpolacyjnego"""
    fig, axs = plt.subplots(2)

    fig.suptitle("Wykres porównawczy (góra), wykres błędu (dół)")
    axs[0].plot(x, y1, label="f. wyjściowa")
    axs[0].plot(x, y2, label="w. interpolacyjny")
    if var_nodes:
        axs[0].scatter(nodes_x, nodes_y, c="black")
    axs[1].plot(x, delta_y, color="red", label="f. błędu")
    for ax in fig.axes:
        ax.grid(True)
        ax.legend(loc="upper left")
    plt.show()


def chebyshev_nodes(n: int, a: float, b: float) -> List[float]:
    """Generuje węzły na podstawie miejsc zerowych wielomianów Czebyszewa."""
    delta1 = (b - a) / 2
    delta2 = (b + a) / 2
    f = [math.cos((i + 0.5) * PI / n) * delta1 + delta2 for i in range(1, n + 1)]
    return sorted(f)


def equidistant_nodes(n: int, a: float, b: float) -> List[float]:
    """Generuje równoodległe węzły."""
    xs = numpy.linspace(a, b, num=n)
    return list(xs)


def random_nodes(n: int, a: float, b: float) -> List[float]:
    """Generuje losowe węzły."""
    xs = [random.uniform(a, b) for i in range(n)]
    return sorted(xs)


def chebyshev_plot(a: float, b: float, n1: int, n2: int) -> None:
    """Generuje wykresy kolejnych węzłów Czebyszewa."""
    x = numpy.linspace(a, b, 10000)
    if n1 < 0 or n2 < 0:
        raise ValueError
    for i in range(n1, n2 + 1):
        axis = plt.plot(x, Chebyshev.basis(i)(x), lw=2, label=f"$T_{{{i}}}$")
    plt.grid(True)
    plt.legend(loc="upper left")
    plt.show()
