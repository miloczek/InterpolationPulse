from hermite_interface import hermite_interpolation
import tkinter as tk
from tkinter.constants import BOTTOM

from utils import clear_win
from lagrange_inteface import lagrange_interpolation
from polynomial_interface import polynomial_parse
from nifs3_interface import nifs3_interpolation
from hermite_interface import hermite_interpolation
from trygonometric_interface import trygonometric_interpolation


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
        command=lambda: trygonometric_interpolation(window),
    )
    btn_exit = tk.Button(
        window, text="Zakończ pracę", font=("Helvetica", "16"), command=window.destroy
    )
    btn_lagrange.pack()
    btn_polynomial.pack()
    btn_nifs3.pack()
    btn_hermite.pack()
    btn_trygonometric.pack()
    btn_exit.pack(side=BOTTOM)
    window.mainloop()