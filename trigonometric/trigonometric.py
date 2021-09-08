from typing_extensions import IntVar
import numpy as np
import math

from numpy.core.fromnumeric import var
import utils
import matplotlib.pyplot as plt
from numpy.lib import polynomial
from typing import List, Tuple

PI = np.pi

SMALL_FLOAT = 1e-3


class Trigonometric:
    """Reprezentacja wielomianu trygonometrycznego."""

    def __init__(self, x: str, y: str) -> None:
        self.x, self.points = utils.str_to_float_list(x), utils.str_to_float_list(y)
        self.n = len(self.x)
        self.aj_coofs, self.bj_coofs = self.generate_a_b_c_cooficients()
        self.trigonometric_polynomial = (
            self.show_interpolation_trigonometric_polynomial()
        )

    def create_aj_cooficients(
        self, cj_coofs: np.array, mid_interval_index: int
    ) -> list:
        """Generuje współczynniki aj."""
        aj_coofs = [2 * cj_coofs[mid_interval_index]]
        for i in range(1, mid_interval_index + 1):
            aj_coofs.append(
                cj_coofs[mid_interval_index + i] + cj_coofs[mid_interval_index - i]
            )
        return aj_coofs

    def create_bj_cooficients(
        self, cj_coofs: np.array, mid_interval_index: int
    ) -> list:
        """Generuje współczynniki bj."""
        bj_coofs = [0]
        for i in range(1, mid_interval_index + 1):
            bj_coofs.append(
                complex(
                    0,
                    cj_coofs[mid_interval_index + i] - cj_coofs[mid_interval_index - i],
                )
            )
        return bj_coofs

    def create_cj_cooficients(self) -> np.array:
        """Generuje współczynniki cj przy użyciu FFT."""
        n = len(self.points)
        ys = np.array(self.points, dtype=np.complex_)
        iteration_start = -(n - 1) // 2
        iteration_end = (n - 1) // 2 + 1

        trigonometric_vals = complex(np.cos(2 * PI / n), np.sin(2 * PI / n))
        fourier_matrix = np.array(
            [
                [trigonometric_vals ** (j * k) for j in range(n)]
                for k in range(iteration_start, iteration_end)
            ]
        )
        cj_coofs = (1 / n) * (np.conj(fourier_matrix) @ ys)
        return cj_coofs

    def replace_small_imag_with_real(
        self, aj_coofs: list, bj_coofs: list
    ) -> Tuple[np.array, np.array]:
        """Zastępuje zbyt małe części urojone współczynników"""
        for i in range(len(aj_coofs)):
            aj_coofs[i] = (
                aj_coofs[i].real if aj_coofs[i].imag < SMALL_FLOAT else aj_coofs[i]
            )

            bj_coofs[i] = (
                bj_coofs[i].real if bj_coofs[i].imag < SMALL_FLOAT else bj_coofs[i]
            )

        return np.array(aj_coofs), np.array(bj_coofs)

    def generate_a_b_c_cooficients(self) -> Tuple[np.array, np.array]:
        """Koordynuje generację współczynników potrzebnych do stworzenia wielomianu interpolacyjnego"""
        cj_coofs = self.create_cj_cooficients()
        mid_interval_index = math.floor(len(self.x) / 2)

        aj_coofs = self.create_aj_cooficients(cj_coofs, mid_interval_index)
        bj_coofs = self.create_bj_cooficients(cj_coofs, mid_interval_index)

        return self.replace_small_imag_with_real(aj_coofs, bj_coofs)

    def show_interpolation_trigonometric_polynomial(self) -> str:
        """Tworzy tekstową reprezentację trygonometrycznego wielomianu interpolacyjnego."""
        polynomial = f"{self.aj_coofs[0]} / 2 "
        for i in range(1, len(self.aj_coofs)):
            polynomial += f"+ {self.aj_coofs[i]} * cos({i} * x) + {self.bj_coofs[i]} * sin({i} * x) "
        return polynomial

    def eval_polynomial_value(self, x):
        """Wylicza kolejną wartość wielomianu interpolacyjnego."""
        return self.aj_coofs[0] / 2 + sum(
            self.aj_coofs[n] * np.cos(n * x) + self.bj_coofs[n] * np.sin(n * x)
            for n in range(1, len(self.aj_coofs))
        )

    def interpolation_plot(self, a: float, b: float, var_nodes: IntVar) -> None:
        """Generuje wykres trygonometrycznego wielomianu interpolacyjnego."""
        x = np.linspace(a, b, 10000)
        y = [self.eval_polynomial_value(i) for i in x]
        plt.suptitle("Wykres funkcji interpolacyjnej")
        plt.grid(True)
        plt.plot(x, y)
        if var_nodes.get():
            plt.scatter(self.x, self.points, c="black")
        plt.show()
