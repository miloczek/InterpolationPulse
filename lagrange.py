import utils
import numpy


class Lagrange:
    """Reprezentacja wielomianu w postaci Lagrange'a."""

    def __init__(self, x: str, function_string: str, precision: str) -> None:
        if precision == "":
            self.x = [float(xi) for xi in x.split(",") if xi != " " and xi != ""]
            self.y, self.f = utils.compute_y(self.x, function_string)
            self.lagrange_polynomial = self.make_interpolation_polynomial()
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
            self.lagrange_polynomial = self.make_interpolation_polynomial()

    # def plot_basic_function_in_xi(self) -> None:
    #     utils.basic_fun_plot(self.x, self.y)

    def plot_basic_function_in_linear_area(self, a: float, b: float) -> None:
        """Generuje wykres funkcji wejściowej."""
        x = numpy.linspace(a, b, 100)
        utils.basic_fun_plot(x, utils.eval_fun(self.f, x))

    def plot_lagrange_in_linear_area(self, a: float, b: float) -> None:
        """Generuje wykres obliczonego wielomianu Lagange'a."""
        x = numpy.linspace(a, b, 100)
        utils.basic_fun_plot(x, utils.eval_fun(self.lagrange_polynomial, x))

    def plot_compare_plot_in_linear_area(self, a: float, b: float) -> None:
        """Generuje wykres porównawczy funkcji wejściowej i wielomianu Lagrange'a."""
        x = numpy.linspace(a, b, 100)
        utils.compare_fun_and_interpolation_plot(
            x, utils.eval_fun(self.f, x), utils.eval_fun(self.lagrange_polynomial, x)
        )

    def make_interpolation_polynomial(self) -> str:
        """Oblicza wielomian Lagrange'a na podstawie węzłów i wartości."""
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
