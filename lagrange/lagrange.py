from typing_extensions import IntVar
import numpy
from numpy.core.fromnumeric import var
import utils
import matplotlib.pyplot as plt


class Lagrange:
    """Reprezentacja wielomianu w postaci Lagrange'a."""

    def __init__(self, x: str, function_string: str, precision: str) -> None:

        if precision == "":
            self.prec = False
            self.x = [float(xi) for xi in x.split(",") if xi != " " and xi != ""]
            self.x.sort()
            self.y, self.f = utils.compute_y(self.x, function_string)
            self.lagrange_polynomial = self.make_interpolation_str_polynomial()
        else:
            self.prec = int(precision)
            self.x = [
                round(float(xi), self.prec)
                for xi in x.split(",")
                if xi != " " and xi != ""
            ]
            self.x.sort()
            self.y, self.f = utils.compute_y_with_prec(
                self.x, function_string, self.prec
            )
            self.lagrange_polynomial = self.make_interpolation_str_polynomial()

    def plot_basic_function_in_linear_area(
        self, a: float, b: float, var_nodes: IntVar
    ) -> None:
        """Generuje wykres funkcji wejściowej."""
        x = numpy.linspace(a, b, 10000)
        if var_nodes.get():
            plt.scatter(self.x, self.y, c="black")
        utils.basic_fun_plot(x, utils.eval_fun(self.f, x))

    def plot_lagrange_in_linear_area(
        self, a: float, b: float, var_nodes: IntVar
    ) -> None:
        """Generuje wykres obliczonego wielomianu Lagange'a."""
        x = numpy.linspace(a, b, 10000)
        if self.prec:
            y = [
                self.eval_interpolation_polynomial_y_value_with_prec(i, self.prec)
                for i in x
            ]
        else:
            y = [self.eval_interpolation_polynomial_y_value(i) for i in x]
        if var_nodes.get():
            plt.scatter(self.x, self.y, c="black")
        utils.basic_fun_plot(x, y)

    def plot_compare_plot_in_linear_area(
        self, a: float, b: float, var_nodes: IntVar
    ) -> None:
        """Generuje wykres porównawczy funkcji wejściowej i wielomianu Lagrange'a."""
        x = numpy.linspace(a, b, 10000)
        if self.prec:
            y = [
                self.eval_interpolation_polynomial_y_value_with_prec(i, self.prec)
                for i in x
            ]
        else:
            y = [self.eval_interpolation_polynomial_y_value(i) for i in x]
        delta_y = [abs(y[i] - utils.eval_fun(self.f, xi)) for i, xi in enumerate(x)]
        var_nodes = var_nodes.get()
        utils.compare_fun_and_interpolation_plot(
            x, utils.eval_fun(self.f, x), y, delta_y, var_nodes, self.x, self.y
        )

    def make_interpolation_str_polynomial(self) -> str:
        """Oblicza tekstowy wielomian Lagrange'a na podstawie węzłów i wartości."""
        n = len(self.x)
        result_poly = "0"
        for i in range(n):
            p = "1"
            for j in range(n):
                if j != i:
                    if self.x[j] < 0:
                        p += f" * (x - ({self.x[j]})) / ({self.x[i]} - ({self.x[j]})) "
                    else:
                        p += f" * (x - {self.x[j]}) / ({self.x[i]} - {self.x[j]}) "
            result_poly += f" + {self.y[i]} * {p} "
        return result_poly

    def eval_interpolation_polynomial_y_value(self, x: float) -> float:
        """Oblicza wartość wielomianu Lagrange'a w podanym punkcie."""
        n = len(self.x)
        value = 0
        for i in range(n):
            p = 1
            for j in range(n):
                if j != i:
                    p *= (x - self.x[j]) / (self.x[i] - self.x[j])
            value += self.y[i] * p
        return value

    def eval_interpolation_polynomial_y_value_with_prec(
        self, x: float, prec: int
    ) -> float:
        """Oblicza wartość wielomianu Lagrange'a w podanym punkcie."""
        n = len(self.x)
        value = 0
        x = round(x, prec)
        for i in range(n):
            p = 1
            for j in range(n):
                if j != i:
                    p *= (x - round(self.x[j], prec)) / (
                        round(self.x[i], prec) - round(self.x[j], prec)
                    )
            value += round(self.y[i], prec) * round(p, prec)
        return round(value, prec)
