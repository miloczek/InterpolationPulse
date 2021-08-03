import numpy as np
import utils
from typing import List


class Nifs3:
    """Reprezentacja NIFS3"""

    def __init__(self, xs: List[str], function_string: str, mode: str) -> None:
        self.x = [float(xi) for xi in xs]
        self.y, self.f = utils.compute_y(self.x, function_string)
        if mode == "three":
            self.polys = self.make_splines3()
        elif mode == "four":
            self.polys = self.make_splines4()

    def make_splines3(self) -> List[str]:
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
        return [
            f"{result[0]} * x ** 3 + {result[1]} * x ** 2 + {result[2]} * x + {result[3]}",
            f"{result[4]} * x ** 3 + {result[5]} * x ** 2 + {result[6]} * x + {result[7]}",
        ]

    def make_splines4(self) -> List[str]:
        pass
