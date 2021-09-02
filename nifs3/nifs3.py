import math
from tkinter import IntVar
from tkinter.constants import E
from typing import List, Union

import matplotlib.pyplot as plt
import numpy as np
import utils


class Nifs3:
    """Reprezentacja NIFS3"""

    def __init__(self, x: str, function_string: str, precision: str) -> None:
        self.prec = False if precision == "" else int(precision)
        self.x = (
            [float(xi) for xi in x.split(",") if xi != " " and xi != ""]
            if not self.prec
            else [
                round(float(xi), self.prec)
                for xi in x.split(",")
                if xi != " " and xi != ""
            ]
        )
        self.x.sort()
        self.x0 = np.linspace(self.x[0], self.x[len(self.x) - 1], num=5000)
        self.y, self.f = (
            utils.compute_y(self.x, function_string)
            if not self.prec
            else utils.compute_y_with_prec(self.x, function_string, self.prec)
        )
        self.M = self.calculate_moments()
        self.make_spline()
        self.prepare_polynomial_string()

    def plot_basic_function_in_linear_area(
        self, a: float, b: float, var_nodes: IntVar
    ) -> None:
        """Generuje wykres funkcji wejściowej."""
        x = np.linspace(a, b, 10000)
        if var_nodes.get():
            plt.scatter(self.x, self.y, c="black")
        utils.basic_fun_plot(x, utils.eval_fun(self.f, x))

    def plot_nifs3_in_linear_area(self, var_nodes: IntVar) -> None:
        """Generuje wykres obliczonej NIFS3."""
        plt.plot(self.x0, self.S_i)
        if var_nodes.get():
            plt.scatter(self.x, self.y, c="black")
        plt.show()

    def plot_compare_plot_in_linear_area(self, var_nodes: IntVar) -> None:
        """Generuje wykres porównawczy funkcji wejściowej i wielomianów NIFS3 dla 3 węzłów."""
        delta_y = [
            abs(self.S_i[i] - utils.eval_fun(self.f, xi))
            for i, xi in enumerate(self.x0)
        ]
        var_nodes = var_nodes.get()
        utils.compare_fun_and_interpolation_plot(
            self.x0,
            utils.eval_fun(self.f, self.x0),
            self.S_i,
            delta_y,
            var_nodes,
            self.x,
            self.y,
        )

    def calculate_moments(self) -> np.array:
        """
        Na podstawie otrzymanych danych tworzymy macierz potrzebną do
        uzyskania tablicy momentów - M.
        Układ rozwiązywany jest metodą Choleskiego w oparciu o:
        https://stackoverflow.com/questions/31543775.
        """
        n = len(self.x)
        x_diff, y_diff = np.diff(self.x), np.diff(self.y)
        L, L_1, M = np.zeros(n), np.zeros(n - 1), np.zeros(n)
        L[0], L_1[0], M[0] = math.sqrt(2 * x_diff[0]), 0, 0

        if not self.prec:
            for i in range(1, n - 1, 1):
                L[i] = math.sqrt(
                    2 * (x_diff[i - 1] + x_diff[i]) - L_1[i - 1] * L_1[i - 1]
                )
                L_1[i] = x_diff[i - 1] / L[i - 1]
                Bi = 6 * (y_diff[i] / x_diff[i] - y_diff[i - 1] / x_diff[i - 1])
                M[i] = (Bi - L_1[i - 1] * M[i - 1]) / L[i]

            L_1[n - 2] = x_diff[-1] / L[n - 2]
            L[n - 1] = math.sqrt(2 * x_diff[-1] - L_1[n - 2] * L_1[n - 2])
            M[n - 1] = (0 - L_1[n - 2] * M[n - 2]) / L[n - 1]
            M[n - 1] = M[n - 1] / L[n - 1]
            for i in range(n - 2, -1, -1):
                M[i] = round((M[i] - L_1[i - 1] * M[i + 1]) / L[i], self.prec)
            return M

        elif self.prec:
            for i in range(1, n - 1, 1):
                L[i] = round(
                    math.sqrt(2 * (x_diff[i - 1] + x_diff[i])), self.prec
                ) - round(L_1[i - 1], self.prec) * round(L_1[i - 1], self.prec)

                L_1[i] = round(x_diff[i - 1], self.prec) / round(L[i - 1], self.prec)
                Bi = round(
                    6 * (y_diff[i] / x_diff[i] - y_diff[i - 1] / x_diff[i - 1]),
                    self.prec,
                )
                M[i] = (
                    Bi - round(L_1[i - 1], self.prec) * round(M[i - 1], self.prec)
                ) / round(L[i], self.prec)

            L_1[n - 2] = round(x_diff[-1] / L[n - 2], self.prec)
            L[n - 1] = round(
                math.sqrt(2 * x_diff[-1] - L_1[n - 2] * L_1[n - 2]), self.prec
            )
            M[n - 1] = round((0 - L_1[n - 2] * M[n - 2]) / L[n - 1], self.prec)
            M[n - 1] = round(M[n - 1] / L[n - 1], self.prec)
            for i in range(n - 2, -1, -1):
                M[i] = round((M[i] - L_1[i - 1] * M[i + 1]) / L[i], self.prec)
            return M

    def put_xs_in_correct_order(self) -> np.array:
        def find_i(x, xs):
            for i in range(len(xs)):
                if x <= xs[i]:
                    return i
            return len(xs)

        return np.clip([find_i(i, self.x) for i in self.x0], 1, len(self.x) - 1)

    def prepare_polynomial_string(self):
        poly_str = ""
        j = 0
        n = len(self.x)
        n_all = len(self.x0)
        for i in range(0, n_all - n_all // n - 1, n_all // n):
            if j < len(self.x) - 1:
                poly_str += (
                    f"{self.S_i_printable[i]} x ∈ [{self.x[j]}, {self.x[j + 1]}] \n"
                )
            else:
                break
            j += 1
        self.poly_str = poly_str

    def make_spline(self):
        """Tworzy Naturalną Interpolacyjną Funkcję Sklejaną Stopnia 3"""

        i = self.put_xs_in_correct_order()

        x_i, x_i_minus_1 = [self.x[num] for num in i], [self.x[num - 1] for num in i]
        y_i, y_i_minus_1 = [self.y[num] for num in i], [self.y[num - 1] for num in i]
        M_i, M_i_minus_1 = [self.M[num] for num in i], [self.M[num - 1] for num in i]
        h_i = (
            [x_i[i] - x_i_minus_1[i] for i in range(len(x_i))]
            if not self.prec
            else [round(x_i[i] - x_i_minus_1[i], self.prec) for i in range(len(x_i))]
        )

        self.S_i, self.S_i_printable = [], []
        for j in range(len(h_i)):
            self.S_i_printable.append(
                f"({h_i[j]}) ** (-1) * ({M_i_minus_1[j]} / 6 * ({x_i[j]} - x)"
                + f" ** 3 + {M_i[j]} / 6 * (x - {x_i_minus_1[j]}) ** 3) +"
                + f" ({y_i_minus_1[j]} / {h_i[j]} - {M_i_minus_1[j]} * {h_i[j]} / 6)"
                + f" * ({x_i[j]} - x) + ({y_i[j]} / {h_i[j]} - {M_i[j]} * {h_i[j]} / 6)"
                + f" * (x - {x_i_minus_1[j]})"
            )
            if not self.prec:
                self.S_i.append(
                    h_i[j] ** (-1)
                    * (
                        M_i_minus_1[j] / 6 * (x_i[j] - self.x0[j]) ** 3
                        + M_i[j] / 6 * (self.x0[j] - x_i_minus_1[j]) ** 3
                    )
                    + (y_i_minus_1[j] / h_i[j] - M_i_minus_1[j] * h_i[j] / 6)
                    * (x_i[j] - self.x0[j])
                    + (y_i[j] / h_i[j] - M_i[j] * h_i[j] / 6)
                    * (self.x0[j] - x_i_minus_1[j])
                )
            else:
                self.S_i.append(
                    round(
                        round(h_i[j] ** (-1), self.prec)
                        * (
                            round(M_i_minus_1[j] / 6, self.prec)
                            * round((x_i[j] - self.x0[j]) ** 3, self.prec)
                            + round(
                                M_i[j] / 6 * (self.x0[j] - x_i_minus_1[j]) ** 3,
                                self.prec,
                            )
                        )
                        + round(
                            y_i_minus_1[j] / h_i[j] - M_i_minus_1[j] * h_i[j] / 6,
                            self.prec,
                        )
                        * round(x_i[j] - self.x0[j], self.prec)
                        + round(y_i[j] / h_i[j] - M_i[j] * h_i[j] / 6, self.prec)
                        * round(self.x0[j] - x_i_minus_1[j], self.prec),
                        self.prec,
                    )
                )
