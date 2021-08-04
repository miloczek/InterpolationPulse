import numpy as np
from numpy.lib.function_base import select
from numpy.testing._private.utils import nulp_diff
import utils
from typing import List, Union


class Nifs3:
    """Reprezentacja NIFS3"""

    def __init__(
        self, xs: List[str], function_string: str, mode: str, precision: str
    ) -> None:
        self.x = [float(xi) for xi in xs]
        self.x.sort()
        self.y, self.f = utils.compute_y(self.x, function_string)
        if mode == "three":
            self.polys = self.make_splines3(precision)
        elif mode == "four":
            self.polys = self.make_splines4(precision)

    def make_splines4(self, precision: str) -> List[str]:
        """Oblicza NIFS3 dla 4 węzłów na podstawie węzłów i wartości"""
        x1, x2, x3, x4 = self.x[0], self.x[1], self.x[2], self.x[3]
        y1, y2, y3, y4 = self.y[0], self.y[1], self.y[2], self.y[4]
        A = np.array(
            [
                [x1 ** 3, x1 ** 2, x1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
                [x2 ** 3, x2 ** 2, x2, 1, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, x2 ** 3, x2 ** 2, x2, 1, 0, 0, 0, 0],
                [0, 0, 0, 0, x3 ** 3, x3 ** 2, x3, 1, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, x3 ** 3, x3 ** 2, x3, 1],
                [0, 0, 0, 0, 0, 0, 0, 0, x4 ** 3, x4 ** 2, x4, 1],
                [3 * x2 ** 2, 2 * x2, 1, 0, -3 * (x2 ** 2), -2 * x2, -1, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 3 * x3 ** 2, 2 * x3, 1, 0, -3 * (x3 ** 2), -2 * x3, -1, 0],
                [6 * x2, 2, 0, 0, -6 * x2, -2, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 6 * x3, 2, 0, 0, -6 * x3, -2, 0, 0],
                [6 * x1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 6 * x4, 2, 0, 0],
            ]
        )

        b = np.array(
            [
                y1,
                y2,
                y2,
                y3,
                y3,
                y4,
                0,
                0,
                0,
                0,
                0,
                0,
            ]
        )

        result = np.linalg.solve(A, b)
        if precision == "":
            return [
                f"{result[0]} * x ** 3 + {result[1]} * x ** 2 + {result[2]} * x + {result[3]}",
                f"{result[4]} * x ** 3 + {result[5]} * x ** 2 + {result[6]} * x + {result[7]}",
                f"{result[8]} * x ** 3 + {result[9]} * x ** 2 + {result[10]} * x + {result[11]}",
            ]
        else:
            precision = int(precision)
            return [
                f"{round(result[0], precision)} * x ** 3 + {round(result[1], precision)} * x ** 2 + {round(result[2], precision)} * x + {round(result[3], precision)}",
                f"{round(result[4], precision)} * x ** 3 + {round(result[5], precision)} * x ** 2 + {round(result[6], precision)} * x + {round(result[7], precision)}",
                f"{round(result[8], precision)} * x ** 3 + {round(result[9], precision)} * x ** 2 + {round(result[10], precision)} * x + {round(result[11], precision)}",
            ]

    def make_splines3(self, precision: str) -> List[str]:
        """Oblicza NIFS3 dla 3 węzłów na podstawie węzłów i wartości"""
        x1, x2, x3 = self.x[0], self.x[1], self.x[2]
        y1, y2, y3 = self.y[0], self.y[1], self.y[2]
        A = np.array(
            [
                [x1 ** 3, x1 ** 2, x1, 1, 0, 0, 0, 0],
                [x2 ** 3, x2 ** 2, x2, 1, 0, 0, 0, 0],
                [0, 0, 0, 0, x2 ** 3, x2 ** 2, x2, 1],
                [0, 0, 0, 0, x3 ** 3, x3 ** 2, x3, 1],
                [3 * x2 ** 2, 2 * x2, 1, 0, -3 * (x2 ** 2), -2 * x2, -1, 0],
                [6 * x2, 2, 0, 0, -6 * x2, -2, 0, 0],
                [6 * x1, 2, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 6 * x3, 2, 0, 0],
            ]
        )

        b = np.array(
            [
                y1,
                y2,
                y2,
                y3,
                0,
                0,
                0,
                0,
            ]
        )
        result = np.linalg.solve(A, b)
        if precision == "":
            return [
                f"{result[0]} * x ** 3 + {result[1]} * x ** 2 + {result[2]} * x + {result[3]}",
                f"{result[4]} * x ** 3 + {result[5]} * x ** 2 + {result[6]} * x + {result[7]}",
            ]
        else:
            precision = int(precision)
            return [
                f"{round(result[0], precision)} * x ** 3 + {round(result[1], precision)} * x ** 2 + {round(result[2], precision)} * x + {round(result[3], precision)}",
                f"{round(result[4], precision)} * x ** 3 + {round(result[5], precision)} * x ** 2 + {round(result[6], precision)} * x + {round(result[7], precision)}",
            ]

    def return_value_nifs33(self, x: Union[float, np.ndarray]):
        """Zwraca wartości NIFS3."""
        if x <= self.x[1]:
            return eval(self.polys[0])
        elif x > self.x[1]:
            return eval(self.polys[1])

    def return_value_nifs34(self, x: Union[float, np.ndarray]):
        """Zwraca wartości NIFS3."""
        if x <= self.x[1]:
            return eval(self.polys[0])
        elif x > self.x[1] and x <= self.x[2]:
            return eval(self.polys[1])
        elif x > self.x[2]:
            return eval(self.polys[2])

    def plot_basic_function_in_linear_area(self, a: float, b: float) -> None:
        """Generuje wykres funkcji wejściowej."""
        x = np.linspace(a, b, 100)
        utils.basic_fun_plot(x, utils.eval_fun(self.f, x))

    def plot_nifs3_in_linear_area3(self, a: float, b: float) -> None:
        """Generuje wykres obliczonej NIFS3."""
        x = np.linspace(a, b, 100)
        utils.basic_fun_plot(x, list(map(self.return_value_nifs33, x)))

    def plot_compare_plot_in_linear_area3(self, a: float, b: float) -> None:
        """Generuje wykres porównawczy funkcji wejściowej i wielomianów NIFS3 dla 3 węzłów."""
        x = np.linspace(a, b, 100)
        utils.compare_fun_and_interpolation_plot(
            x, utils.eval_fun(self.f, x), list(map(self.return_value_nifs33, x))
        )
