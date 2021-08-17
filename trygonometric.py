import numpy as np
import math
import matplotlib.pyplot as plt
from numpy.lib import polynomial

PI = np.pi
SMALL_FLOAT = np.finfo(float).eps


class Trygonometric:
    """Reprezentacja wielomianu trygonometrycznego."""

    def __init__(self, data: list, mode: str) -> None:
        if mode == "pi":
            self.x, self.n = float(data[0]), int(data[1])
            self.n = self.n + 1 if self.n % 2 == 0 else self.n
            self.points = self.return_list_of_points(self.x, self.n)
            self.aj_coofs, self.bj_coofs = self.get_sin_cos_representation(self.points)
            self.trygonometric_polynomial = (
                self.show_interpolation_trygonometric_polynomial(
                    self.aj_coofs, self.bj_coofs
                )
            )
            # plot_sin_cos_representation(A, B, points)

    def create_aj_cooficients(self, cj_coofs, mid_interval_index):
        aj_coofs = [2 * cj_coofs[mid_interval_index]]
        for i in range(1, mid_interval_index + 1):
            aj_coofs.append(
                cj_coofs[mid_interval_index + i] + cj_coofs[mid_interval_index - i]
            )
        return aj_coofs

    def create_bj_cooficients(self, cj_coofs, mid_interval_index):
        bj_coofs = [0]
        for i in range(1, mid_interval_index + 1):
            bj_coofs.append(
                complex(
                    0,
                    cj_coofs[mid_interval_index + i] - cj_coofs[mid_interval_index - i],
                )
            )
        return bj_coofs

    def create_cj_cooficients(self, points):
        n = len(points)
        ys = np.array(points, dtype=np.complex_)
        iteration_start = -(n - 1) // 2
        iteration_end = (n - 1) // 2 + 1

        w = complex(np.cos(2 * PI / n), np.sin(2 * PI / n))
        fourier_matrix = np.array(
            [
                [w ** (j * k) for j in range(n)]
                for k in range(iteration_start, iteration_end)
            ]
        )
        cj_coofs = (1 / n) * (np.conj(fourier_matrix) @ ys)
        return cj_coofs

    def replace_small_imag_with_real(self, aj_coofs, bj_coofs):
        for i in range(len(aj_coofs)):
            aj_coofs[i] = (
                aj_coofs[i].real if aj_coofs[i].imag < SMALL_FLOAT else aj_coofs[i]
            )

            bj_coofs[i] = (
                bj_coofs[i].real if bj_coofs[i].imag < SMALL_FLOAT else bj_coofs[i]
            )

        return np.array(aj_coofs), np.array(bj_coofs)

    def get_sin_cos_representation(self, points):
        cj_coofs = self.create_cj_cooficients(points)
        mid_interval_index = math.floor(len(cj_coofs) / 2)

        aj_coofs = self.create_aj_cooficients(cj_coofs, mid_interval_index)
        bj_coofs = self.create_bj_cooficients(cj_coofs, mid_interval_index)

        return self.replace_small_imag_with_real(aj_coofs, bj_coofs)

    def show_interpolation_trygonometric_polynomial(self, A, B):
        polynomial = f"{A[0]} / 2 "
        for i in range(1, len(A)):
            polynomial += f"+ {A[i]} * cos({i} * x) + {B[i]} * sin({i} * x) "
        return polynomial

    def eval_sin_cos_representation(self, t, A, B):
        return A[0] / 2 + sum(
            A[n] * np.cos(n * t) + B[n] * np.sin(n * t) for n in range(1, len(A))
        )

    def plot_sin_cos_representation(self, start=-10, end=10):
        Xs = np.linspace(start, end, 5000)
        Ys = [
            self.eval_sin_cos_representation(t, self.aj_coofs, self.bj_coofs)
            for t in Xs
        ]

        n = len(self.points)
        x_points = np.array([(2 * PI * i) / n for i in range(n)])

        plt.figure(figsize=(14, 7))
        plt.grid(True)
        plt.plot(Xs, Ys)
        plt.scatter(x_points, self.points, c="black")
        plt.show()

    def return_list_of_points(self, x, n):
        return [x * PI * i / n for i in range(n)]

    # if __name__ == "__main__":
    #     # points = list(map(float, sys.argv[1:]))
    #     # Xs = np.linspace(-10, 10, 5000)
    #     points = return_list_of_points(43)
    #     A, B = get_sin_cos_representation(points)

    #     plot_sin_cos_representation(A, B, points)
