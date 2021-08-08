from operator import add
import numpy
from numpy.lib import polynomial
import utils


class Hermite:
    """Reprezentacja wielomianu w postaci Hermite'a."""

    def __init__(self, x: str, function_string: str, precision: str) -> None:
        if precision == "":
            self.x = [float(xi) for xi in x.split(",") if xi != " " and xi != ""]
            self.y, self.f = utils.compute_y(self.x, function_string)
            self.hermite_polynomial = self.make_interpolation_polynomial()
        else:
            precision = int(precision)
            self.x = [
                round(float(xi), precision)
                for xi in x.split(",")
                if xi != " " and xi != ""
            ]
            self.y, self.f = utils.compute_y_with_prec(
                self.x, function_string, precision
            )
            self.hermite_polynomial = self.make_interpolation_polynomial_with_prec(
                precision
            )

    def plot_basic_function_in_linear_area(self, a: float, b: float) -> None:
        """Generuje wykres funkcji wejściowej."""
        x = numpy.linspace(a, b, 100)
        utils.basic_fun_plot(x, utils.eval_fun(self.f, x))

    def plot_lagrange_in_linear_area(self, a: float, b: float) -> None:
        """Generuje wykres obliczonego wielomianu Hermite'a."""
        x = numpy.linspace(a, b, 100)
        utils.basic_fun_plot(x, utils.eval_fun(self.hermite_polynomial, x))

    def plot_compare_plot_in_linear_area(self, a: float, b: float) -> None:
        """Generuje wykres porównawczy funkcji wejściowej i wielomianu Hermite'a."""
        x = numpy.linspace(a, b, 100)
        utils.compare_fun_and_interpolation_plot(
            x, utils.eval_fun(self.f, x), utils.eval_fun(self.hermite_polynomial, x)
        )

    def make_interpolation_polynomial(self) -> str:
        """Buduje tablicę ilorazów różnicowych, oblicza wielomian Hermite'a na podstawie węzłów i wartości."""
        hermite_coofincients = []
        polynomial = ""
        n = len(self.x)
        table_of_diffs = numpy.zeros(shape=(2 * n + 1, 2 * n + 1))
        for i in range(0, 2 * n, 2):
            table_of_diffs[i][0] = self.x[i // 2]
            table_of_diffs[i + 1][0] = self.x[i // 2]
            table_of_diffs[i][1] = self.y[i // 2]
            table_of_diffs[i + 1][1] = self.y[i // 2]
        for i in range(2, 2 * n + 1):
            for j in range(1 + (i - 2), 2 * n):
                if i == 2 and j % 2 == 1:
                    table_of_diffs[j][i] = utils.eval_derivative_fun(
                        self.f, self.x[j // 2]
                    )
                else:
                    table_of_diffs[j][i] = (
                        table_of_diffs[j][i - 1] - table_of_diffs[j - 1][i - 1]
                    ) / (table_of_diffs[j][0] - table_of_diffs[(j - 1) - (i - 2)][0])
        diagonal = 1
        for i in range(len(table_of_diffs) - 1):
            hermite_coofincients.append(table_of_diffs[i][diagonal])
            diagonal += 1
        polynomial += str(hermite_coofincients[0])
        add_x = True
        x_index = 0
        x_str = ""
        for i in range(1, len(hermite_coofincients)):
            if add_x:
                if self.x[x_index] > 0:
                    x_str += f" * (x-{self.x[x_index]})"
                else:
                    x_str += f" * (x-({self.x[x_index]}))"
                add_x = False
                if hermite_coofincients[i] >= 0:
                    polynomial += f" + {hermite_coofincients[i]}{x_str}"
                if hermite_coofincients[i] < 0:
                    polynomial += f" + ({hermite_coofincients[i]}){x_str}"
            elif not add_x:
                x_str += "**2"
                add_x = True
                x_index += 1
                if hermite_coofincients[i] >= 0:
                    polynomial += f" + {hermite_coofincients[i]} {x_str}"
                if hermite_coofincients[i] < 0:
                    polynomial += f" + ({hermite_coofincients[i]}) {x_str}"
        return polynomial

    def make_interpolation_polynomial_with_prec(self, precision) -> str:
        """Buduje tablicę ilorazów różnicowych, oblicza wielomian Hermite'a z zadaną
        precyzją na podstawie węzłów i wartości."""
        hermite_coofincients = []
        polynomial = ""
        n = len(self.x)
        table_of_diffs = numpy.zeros(shape=(2 * n + 1, 2 * n + 1))
        for i in range(0, 2 * n, 2):
            table_of_diffs[i][0] = self.x[i // 2]
            table_of_diffs[i + 1][0] = self.x[i // 2]
            table_of_diffs[i][1] = self.y[i // 2]
            table_of_diffs[i + 1][1] = self.y[i // 2]
        for i in range(2, 2 * n + 1):
            for j in range(1 + (i - 2), 2 * n):
                if i == 2 and j % 2 == 1:
                    table_of_diffs[j][i] = utils.eval_derivative_fun_with_prec(
                        self.f, self.x[j // 2], precision
                    )
                else:
                    table_of_diffs[j][i] = round(
                        (table_of_diffs[j][i - 1] - table_of_diffs[j - 1][i - 1])
                        / (table_of_diffs[j][0] - table_of_diffs[(j - 1) - (i - 2)][0]),
                        precision,
                    )
        diagonal = 1
        for i in range(len(table_of_diffs) - 1):
            hermite_coofincients.append(round(table_of_diffs[i][diagonal], precision))
            diagonal += 1
        polynomial += str(hermite_coofincients[0])
        add_x = True
        x_index = 0
        x_str = ""
        for i in range(1, len(hermite_coofincients)):
            if add_x:
                if self.x[x_index] > 0:
                    x_str += f" * (x-{self.x[x_index]})"
                else:
                    x_str += f" * (x-({self.x[x_index]}))"
                add_x = False
                if hermite_coofincients[i] >= 0:
                    polynomial += f" + {hermite_coofincients[i]}{x_str}"
                if hermite_coofincients[i] < 0:
                    polynomial += f" + ({hermite_coofincients[i]}){x_str}"
            elif not add_x:
                x_str += "**2"
                add_x = True
                x_index += 1
                if hermite_coofincients[i] >= 0:
                    polynomial += f" + {hermite_coofincients[i]} {x_str}"
                if hermite_coofincients[i] < 0:
                    polynomial += f" + ({hermite_coofincients[i]}) {x_str}"
        return polynomial
