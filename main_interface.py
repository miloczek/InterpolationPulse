import tkinter as tk
from tkinter.constants import BOTTOM

from utils import clear_win
from lagrange.lagrange_inteface import lagrange_interpolation
from polynomial.polynomial_interface import polynomial_parse
from nifs3.nifs3_interface import nifs3_interpolation
from hermite.hermite_interface import hermite_interpolation
from trigonometric.trigonometric_interface import trigonometric_interpolation
from chebyshev.chebyshev_interface import chebyshev_polynomials


def main(window: tk.Tk) -> None:
    """Główna funkcja, spajająca wszystkie funkcjonalności i
    porządkująca interfejsy."""
    clear_win(window)

    lbl_instruction = tk.Label(
        window,
        text="Proszę o wybranie jednej z dostępnych opcji:",
        font=("Helvetica", "24"),
    )
    lbl_instruction.pack()
    btn_lagrange = tk.Button(
        window,
        text="Interpolacja Lagrange'a",
        font=("Helvetica", "16"),
        command=lambda: lagrange_interpolation(window),
    )
    btn_polynomial = tk.Button(
        window,
        text="Postacie wielomianów",
        font=("Helvetica", "16"),
        command=lambda: polynomial_parse(window),
    )

    btn_nifs3 = tk.Button(
        window,
        text="NIFS 3",
        font=("Helvetica", "16"),
        command=lambda: nifs3_interpolation(window),
    )

    btn_hermite = tk.Button(
        window,
        text="Interpolacja Hermite'a",
        font=("Helvetica", "16"),
        command=lambda: hermite_interpolation(window),
    )

    btn_trygonometric = tk.Button(
        window,
        text="Interpolacja trygonometryczna",
        font=("Helvetica", "16"),
        command=lambda: trigonometric_interpolation(window),
    )

    btn_chebyshev = tk.Button(
        window,
        text="Wielomiany Czebyszewa",
        font=("Helvetica", "16"),
        command=lambda: chebyshev_polynomials(window),
    )

    btn_exit = tk.Button(
        window, text="Zakończ pracę", font=("Helvetica", "16"), command=window.destroy
    )
    btn_lagrange.pack()
    btn_polynomial.pack()
    btn_nifs3.pack()
    btn_hermite.pack()
    btn_trygonometric.pack()
    btn_chebyshev.pack()
    btn_exit.pack(side=BOTTOM)
    window.mainloop()