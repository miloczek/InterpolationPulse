from typing import List
import utils
from typing import List

class Lagrange:
    def __init__(self, x: str, function_string: str) -> None:
        self.x = [int(xi) for xi in  x.split(",")]
        self.y = utils.compute_y(self.x, function_string)