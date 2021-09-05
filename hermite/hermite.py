from typing_extensions import IntVar
import numpy
import utils
import matplotlib.pyplot as plt


class Hermite:
    """Reprezentacja wielomianu w postaci Hermite'a."""

    def __init__(self, x: str, y: str, y_prim: str, precision: str) -> None:
        if precision == "":
            self.prec = False
            self.x, self.y, self.y_prim = (
                utils.str_to_float_list(x),
                utils.str_to_float_list(y),
                utils.str_to_float_list(y_prim),
            )
            self.make_interpolation_polynomial()

        else:
            self.prec = int(precision)
            self.x, self.y, self.y_prim = (
                utils.str_to_float_list(x),
                utils.str_to_float_list(y),
                utils.str_to_float_list(y_prim),
            )
            self.x, self.y, self.y_prim = (
                utils.round_list_of_floats(self.x, self.prec),
                utils.round_list_of_floats(self.y, self.prec),
                utils.round_list_of_floats(self.y_prim, self.prec),
            )
            self.make_interpolation_polynomial_with_prec()

    def eval_interpolation_polynomial_y_value(self, x: float) -> float:
        """Oblicza wartość wielomianu interpolacyjnego w punkcie x."""
        result = self.hermite_cooficients[0]
        add_x = True
        x_pos = ""
        x_index = 0
        for i in range(1, len(self.hermite_cooficients)):
            if add_x:
                x_pos += f" * (x-{self.x[x_index]})"
                add_x = False
                result += eval(f"{self.hermite_cooficients[i]} {x_pos}")
            elif not add_x:
                x_pos += "**2"
                add_x = True
                x_index += 1
                result += eval(f"{self.hermite_cooficients[i]} {x_pos}")
        return result

    def plot_basic_function_in_linear_area(
        self, a: float, b: float, fun_str: str, var_nodes: IntVar
    ) -> None:
        """Generuje wykres funkcji wejściowej."""
        x = numpy.linspace(a, b, 10000)
        if var_nodes.get():
            plt.scatter(self.x, self.y, c="black")
        utils.basic_fun_plot(x, utils.eval_fun(fun_str, x))

    def plot_hermite_in_linear_area(
        self, a: float, b: float, var_nodes: IntVar
    ) -> None:
        """Generuje wykres obliczonego wielomianu Hermite'a."""
        x = numpy.linspace(a, b, 1000)
        y = [self.eval_interpolation_polynomial_y_value(i) for i in x]
        if var_nodes.get():
            plt.scatter(self.x, self.y, c="black")
        utils.basic_fun_plot(x, y)

    def plot_compare_plot_in_linear_area(
        self, a: float, b: float, fun_str: str, var_nodes: IntVar
    ) -> None:
        """Generuje wykres porównawczy funkcji wejściowej i wielomianu Hermite'a."""
        x = numpy.linspace(a, b, 1000)

        y = [self.eval_interpolation_polynomial_y_value(i) for i in x]
        delta_y = [abs(y[i] - utils.eval_fun(fun_str, xi)) for i, xi in enumerate(x)]
        var_nodes = var_nodes.get()
        utils.compare_fun_and_interpolation_plot(
            x, utils.eval_fun(fun_str, x), y, delta_y, var_nodes, self.x, self.y
        )

    def make_interpolation_polynomial(self) -> str:
        """Buduje tablicę ilorazów różnicowych, oblicza wielomian Hermite'a na podstawie węzłów i wartości."""
        coofs = []
        polynomial = ""
        n = len(self.x)
        self.table_of_diffs = numpy.zeros(shape=(2 * n + 1, 2 * n + 1))
        for i in range(0, 2 * n, 2):
            self.table_of_diffs[i][0] = self.x[i // 2]
            self.table_of_diffs[i + 1][0] = self.x[i // 2]
            self.table_of_diffs[i][1] = self.y[i // 2]
            self.table_of_diffs[i + 1][1] = self.y[i // 2]
        for i in range(2, 2 * n + 1):
            for j in range(1 + (i - 2), 2 * n):
                if i == 2 and j % 2 == 1:
                    self.table_of_diffs[j][i] = self.y_prim[j // 2]
                else:
                    self.table_of_diffs[j][i] = (
                        self.table_of_diffs[j][i - 1]
                        - self.table_of_diffs[j - 1][i - 1]
                    ) / (
                        self.table_of_diffs[j][0]
                        - self.table_of_diffs[(j - 1) - (i - 2)][0]
                    )
        diagonal = 1
        for i in range(len(self.table_of_diffs) - 1):
            coofs.append(self.table_of_diffs[i][diagonal])
            diagonal += 1
        self.hermite_cooficients = coofs
        polynomial += str(self.hermite_cooficients[0])
        add_x = True
        x_index = 0
        x_str = ""
        for i in range(1, len(self.hermite_cooficients)):
            if add_x:
                if self.x[x_index] > 0:
                    x_str += f" * (x-{self.x[x_index]})"
                else:
                    x_str += f" * (x-({self.x[x_index]}))"
                add_x = False
                if self.hermite_cooficients[i] >= 0:
                    polynomial += f" + {self.hermite_cooficients[i]}{x_str}"
                if self.hermite_cooficients[i] < 0:
                    polynomial += f" + ({self.hermite_cooficients[i]}){x_str}"
            elif not add_x:
                x_str += "**2"
                add_x = True
                x_index += 1
                if self.hermite_cooficients[i] >= 0:
                    polynomial += f" + {self.hermite_cooficients[i]} {x_str}"
                if self.hermite_cooficients[i] < 0:
                    polynomial += f" + ({self.hermite_cooficients[i]}) {x_str}"
        self.printable_polynomial = polynomial

    def make_interpolation_polynomial_with_prec(self) -> str:
        """Buduje tablicę ilorazów różnicowych, oblicza wielomian Hermite'a z zadaną
        precyzją na podstawie węzłów i wartości."""
        coofs = []
        polynomial = ""
        n = len(self.x)
        self.table_of_diffs = numpy.zeros(shape=(2 * n + 1, 2 * n + 1))
        for i in range(0, 2 * n, 2):
            self.table_of_diffs[i][0] = self.x[i // 2]
            self.table_of_diffs[i + 1][0] = self.x[i // 2]
            self.table_of_diffs[i][1] = self.y[i // 2]
            self.table_of_diffs[i + 1][1] = self.y[i // 2]
        for i in range(2, 2 * n + 1):
            for j in range(1 + (i - 2), 2 * n):
                if i == 2 and j % 2 == 1:
                    self.table_of_diffs[j][i] = self.y_prim[j // 2]
                else:
                    self.table_of_diffs[j][i] = round(
                        (
                            self.table_of_diffs[j][i - 1]
                            - self.table_of_diffs[j - 1][i - 1]
                        )
                        / (
                            self.table_of_diffs[j][0]
                            - self.table_of_diffs[(j - 1) - (i - 2)][0]
                        ),
                        self.prec,
                    )
        for i in range(len(self.table_of_diffs)):
            for j in range(len(self.table_of_diffs)):
                self.table_of_diffs[i][j] = round(self.table_of_diffs[i][j], self.prec)
        diagonal = 1
        for i in range(len(self.table_of_diffs) - 1):
            coofs.append(self.table_of_diffs[i][diagonal])
            diagonal += 1
        self.hermite_cooficients = coofs
        polynomial += str(self.hermite_cooficients[0])
        add_x = True
        x_index = 0
        x_str = ""
        for i in range(1, len(self.hermite_cooficients)):
            if add_x:
                if self.x[x_index] > 0:
                    x_str += f" * (x-{self.x[x_index]})"
                else:
                    x_str += f" * (x-({self.x[x_index]}))"
                add_x = False
                if self.hermite_cooficients[i] >= 0:
                    polynomial += f" + {self.hermite_cooficients[i]}{x_str}"
                if self.hermite_cooficients[i] < 0:
                    polynomial += f" + ({self.hermite_cooficients[i]}){x_str}"
            elif not add_x:
                x_str += "**2"
                add_x = True
                x_index += 1
                if self.hermite_cooficients[i] >= 0:
                    polynomial += f" + {self.hermite_cooficients[i]} {x_str}"
                if self.hermite_cooficients[i] < 0:
                    polynomial += f" + ({self.hermite_cooficients[i]}) {x_str}"
        self.printable_polynomial = polynomial
