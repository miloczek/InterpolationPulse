import numpy as np
import math
import utils
import matplotlib.pyplot as plt
from numpy.lib import polynomial
from typing import List, Tuple

PI = np.pi

SMALL_FLOAT = 1e-3


class Trygonometric:
    """Reprezentacja wielomianu trygonometrycznego."""

    def __init__(self, f: str, n: str) -> None:
        n = int(n)
        self.n = n + 1 if n % 2 == 0 else n
        self.x_points = np.linspace(-10, 10, n)
        self.points, self.f = utils.compute_y(self.x_points, f)
        self.aj_coofs, self.bj_coofs = self.generate_a_b_c_cooficients()
        self.trygonometric_polynomial = (
            self.show_interpolation_trygonometric_polynomial()
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

        trygonometric_vals = complex(np.cos(2 * PI / n), np.sin(2 * PI / n))
        fourier_matrix = np.array(
            [
                [trygonometric_vals ** (j * k) for j in range(n)]
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
        mid_interval_index = math.floor(len(cj_coofs) / 2)

        aj_coofs = self.create_aj_cooficients(cj_coofs, mid_interval_index)
        bj_coofs = self.create_bj_cooficients(cj_coofs, mid_interval_index)

        return self.replace_small_imag_with_real(aj_coofs, bj_coofs)

    def show_interpolation_trygonometric_polynomial(self) -> str:
        polynomial = f"{self.aj_coofs[0]} / 2 "
        for i in range(1, len(self.aj_coofs)):
            polynomial += f"+ {self.aj_coofs[i]} * cos({i} * x) + {self.bj_coofs[i]} * sin({i} * x) "
        return polynomial

    def eval_sin_cos_representation(self, t, A, B):
        return A[0] / 2 + sum(
            A[n] * np.cos(n * t) + B[n] * np.sin(n * t) for n in range(1, len(A))
        )

    def compare_fun_and_interpolation_plot(self, a, b):
        x = np.linspace(a, b, 10000)
        y = [
            self.eval_sin_cos_representation(i, self.aj_coofs, self.bj_coofs) for i in x
        ]
        plt.suptitle("Wykres funkcji interpolacyjnej")
        plt.grid(True)
        plt.plot(x, y)
        plt.scatter(self.x_points, self.points, c="black")
        plt.show()
